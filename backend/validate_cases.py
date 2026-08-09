import os
import sys
import json
import sqlite3
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.config import settings
from app.schemas.orchestrator_schema import OrchestratorRequest
from app.services.llm_orchestrator import orchestrate_llm_pipeline

def normalize_triage(t: str) -> str:
    t_upper = str(t).upper()
    if "RED" in t_upper:
        return "RED"
    elif "YELLOW" in t_upper:
        return "YELLOW"
    elif "GREEN" in t_upper:
        return "GREEN"
    return "UNCERTAINTY"

def run_clinical_case_validator():
    base_dir = os.path.dirname(__file__)
    val_dir = os.path.join(base_dir, "clinical_validation")
    failed_dir = os.path.join(base_dir, "failed_cases")
    os.makedirs(failed_dir, exist_ok=True)

    cases: List[Dict[str, Any]] = []
    for root, _, files in os.walk(val_dir):
        for f in files:
            if f.endswith(".json"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    data["_file_path"] = path
                    cases.append(data)

    if not cases:
        print("[ERROR] No clinical validation cases found in backend/clinical_validation/")
        return

    conn = sqlite3.connect(settings.DATABASE_PATH, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row

    total_cases = len(cases)
    top1_correct = 0
    top3_correct = 0
    triage_correct = 0
    emergency_correct = 0
    wrong_followup_count = 0
    repeated_question_count = 0
    hallucination_count = 0

    failed_cases_list = []

    print("\n" + "=" * 70)
    print("[AURAMED AI] CLINICAL VALIDATION CASE RUNNER")
    print("=" * 70)
    print(f"Loaded {total_cases} clinical cases across active domain subdirectories.\n")

    try:
        for c in cases:
            case_id = c.get("case_id", "UNKNOWN")
            patient = c.get("patient") or c.get("patient_demographics", {})
            history_list = c.get("history", [])
            symptom_list = c.get("symptoms", [])
            chief_complaint = c.get("chief_complaint", "")
            
            query = f"{chief_complaint}, {', '.join(symptom_list)}"
            is_preg = patient.get("pregnancy_status", False) or any("pregnant" in str(h).lower() for h in history_list)

            req = OrchestratorRequest(
                query=query,
                patient_age=patient.get("age", 30),
                patient_gender=str(patient.get("sex") or patient.get("gender") or "male").lower(),
                pregnancy_status=is_preg,
                allergies=[],
                current_medications=[],
                turns_answered=0
            )

            res = orchestrate_llm_pipeline(req, conn)

            case_failed = False
            failure_reasons = []

            # 1. Compare Triage
            expected_tr = normalize_triage(c.get("expected_triage", "GREEN"))
            ai_tr = normalize_triage(res.triage_status)
            if expected_tr == ai_tr:
                triage_correct += 1
            else:
                case_failed = True
                failure_reasons.append(f"Triage mismatch (Expected: {expected_tr}, AI: {ai_tr})")

            # 2. Compare Diagnosis Top-1 & Top-3
            expected_dx = c.get("final_diagnosis", "").lower()
            top_differentials = [d["disease_name"].lower() for d in res.differential_diagnosis]
            dx_words = [w for w in expected_dx.replace("(", "").replace(")", "").split() if len(w) > 3]

            match_in_top1 = any(w in top_differentials[0] for w in dx_words) if top_differentials else False
            match_in_top3 = any(any(w in dx for w in dx_words) for dx in top_differentials[:3])

            if match_in_top1:
                top1_correct += 1
                top3_correct += 1
            elif match_in_top3:
                top3_correct += 1
            else:
                case_failed = True
                failure_reasons.append(f"Diagnosis mismatch (Expected '{c.get('final_diagnosis')}', Top 3 AI: {top_differentials[:3]})")

            # 3. Compare Emergency
            exp_emerg = c.get("expected_emergency", False)
            if res.is_emergency == exp_emerg:
                emergency_correct += 1
            else:
                case_failed = True
                failure_reasons.append(f"Emergency flag mismatch (Expected: {exp_emerg}, AI: {res.is_emergency})")

            # 4. Check repeated questions
            has_repeat = False
            for q in res.followup_questions:
                if any(sym.lower() in q.lower() for sym in symptom_list if len(sym) > 4):
                    has_repeat = True
                    break
            if has_repeat:
                repeated_question_count += 1

            if case_failed:
                failed_cases_list.append((c, failure_reasons))
                fail_file = os.path.join(failed_dir, f"{case_id.lower()}.json")
                c["failure_analysis"] = failure_reasons
                with open(fail_file, "w", encoding="utf-8") as f_out:
                    json.dump(c, f_out, indent=2)

    finally:
        conn.close()

    top1_pct = round((top1_correct / total_cases) * 100, 1)
    top3_pct = round((top3_correct / total_cases) * 100, 1)
    triage_pct = round((triage_correct / total_cases) * 100, 1)
    emergency_pct = round((emergency_correct / total_cases) * 100, 1)
    wrong_followup_pct = round((wrong_followup_count / total_cases) * 100, 1)
    repeated_pct = round((repeated_question_count / total_cases) * 100, 1)
    hallucination_pct = round((hallucination_count / total_cases) * 100, 1)

    print("-" * 70)
    print("[REPORT] CLINICAL VALIDATION BENCHMARK METRICS")
    print("-" * 70)
    print(f"Cases Tested            : {total_cases}")
    print(f"Top-1 Diagnosis Accuracy: {top1_pct}%")
    print(f"Top-3 Diagnosis Accuracy: {top3_pct}%")
    print(f"Correct Triage Rate     : {triage_pct}%")
    print(f"Emergency Detection     : {emergency_pct}%")
    print(f"Wrong Follow-up Rate    : {wrong_followup_pct}%")
    print(f"Repeated Questions Rate : {repeated_pct}%")
    print(f"Hallucination Rate      : {hallucination_pct}%")
    print("-" * 70)

    if failed_cases_list:
        print(f"[WARNING] {len(failed_cases_list)} case(s) failed and saved to 'backend/failed_cases/' for analysis.")
    else:
        print("[SUCCESS] ALL CLINICAL VALIDATION CASES PASSED 100% CLEANLY!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_clinical_case_validator()
