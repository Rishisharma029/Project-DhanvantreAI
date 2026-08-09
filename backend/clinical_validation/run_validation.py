"""
AuraMed AI — Clinical Validation Runner v1.0
=============================================
Runs the full AuraMed pipeline against every case in clinical_validation/
and measures accuracy across all acceptance criteria.

Metrics tracked:
  - triage_accuracy       : Correct triage classification
  - top1_accuracy         : Expected diagnosis = rank #1
  - top3_accuracy         : Expected diagnosis in top 3
  - emergency_detection   : Emergency caught correctly
  - false_emergency_rate  : Emergency triggered on non-emergency
  - hallucination_count   : Any drug/disease from hallucination_check found
  - avg_questions_asked   : Mean follow-up questions per case
  - medicine_suppression  : Correctly withheld medicine when confidence < 70%
  - failure_cases         : All failed cases saved for review

Run: python clinical_validation/run_validation.py
"""
import json
import os
import sys
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Adjust path for backend imports
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.config import settings
from app.schemas.orchestrator_schema import OrchestratorRequest
from app.services.llm_orchestrator import orchestrate_llm_pipeline

VALIDATION_DIR = os.path.dirname(os.path.abspath(__file__))
FAILURE_DIR = os.path.join(VALIDATION_DIR, "failures")
os.makedirs(FAILURE_DIR, exist_ok=True)

TRIAGE_MAP = {
    "RED": "RED_URGENT",
    "RED_URGENT": "RED_URGENT",
    "YELLOW": "YELLOW_MODERATE",
    "YELLOW_MODERATE": "YELLOW_MODERATE",
    "GREEN": "GREEN_STABLE",
    "GREEN_STABLE": "GREEN_STABLE",
}


def normalize_triage(t: str) -> str:
    return TRIAGE_MAP.get(t.upper(), t.upper())


def load_all_cases() -> List[Dict[str, Any]]:
    """Loads all JSON case files from all specialty subdirectories."""
    cases = []
    for specialty_dir in os.listdir(VALIDATION_DIR):
        full_path = os.path.join(VALIDATION_DIR, specialty_dir)
        if not os.path.isdir(full_path) or specialty_dir == "failures":
            continue
        for fname in os.listdir(full_path):
            if fname.endswith(".json"):
                fpath = os.path.join(full_path, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        case = json.load(f)
                        case["_file"] = fpath
                        cases.append(case)
                except Exception as e:
                    print(f"  [WARN] Failed to load {fpath}: {e}")
    return cases


def run_pipeline_on_case(case: Dict[str, Any], conn: sqlite3.Connection) -> Dict[str, Any]:
    """Runs the AuraMed pipeline on a single validation case."""
    patient = case.get("patient", {})
    symptoms = case.get("presenting_symptoms", [])
    history = case.get("history", {})
    vitals = case.get("vitals", {})

    # Build query from chief complaint + symptoms
    chief = case.get("chief_complaint", "")
    symptom_text = "; ".join(symptoms[:4])
    query = f"{chief}. Symptoms: {symptom_text}"

    # Handle history which can be a dict or a list depending on case source
    if isinstance(history, list):
        chronic = history
        allergies = []
        meds = []
    else:
        chronic = history.get("past_medical", [])
        allergies = history.get("allergies", [])
        meds = history.get("medications", [])

    req = OrchestratorRequest(
        query=query,
        patient_age=patient.get("age"),
        patient_gender=patient.get("sex", "").lower() if patient.get("sex") else None,
        pregnancy_status=(patient.get("sex", "").lower() == "female"
                          and "pregnancy" in case.get("specialty", "").lower()) if patient.get("sex") else False,
        allergies=allergies,
        chronic_diseases=chronic,
        current_medications=meds,
        turns_answered=0,
    )

    result = orchestrate_llm_pipeline(req, conn)
    return {
        "triage_status": result.triage_status,
        "is_emergency": result.is_emergency,
        "differential_diagnosis": result.differential_diagnosis,
        "confidence_score": result.confidence_score,
        "followup_questions": result.followup_questions,
        "recommended_medicines": result.recommended_medicines,
        "medicine_recommendation_suppressed": result.medicine_recommendation_suppressed,
        "syndrome_detected": result.syndrome_detected,
    }


def evaluate_case(case: Dict[str, Any], pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates pipeline output against expected case criteria."""
    results = {
        "case_id": case.get("case_id", "UNKNOWN"),
        "specialty": case.get("specialty", ""),
        "final_diagnosis": case.get("final_diagnosis", ""),
        "passes": [],
        "failures": [],
        "warnings": [],
    }

    expected_triage = normalize_triage(case.get("expected_triage", "GREEN"))
    actual_triage = normalize_triage(pipeline_output["triage_status"])

    # 1. Triage check
    if actual_triage == expected_triage:
        results["passes"].append(f"TRIAGE_CORRECT: {actual_triage}")
    else:
        results["failures"].append(
            f"TRIAGE_WRONG: expected={expected_triage}, got={actual_triage}"
        )

    # 2. Emergency check
    expected_emergency = case.get("expected_emergency", False)
    actual_emergency = pipeline_output["is_emergency"]
    if actual_emergency == expected_emergency:
        results["passes"].append(f"EMERGENCY_CORRECT: {actual_emergency}")
    else:
        if expected_emergency and not actual_emergency:
            results["failures"].append("MISSED_EMERGENCY: should have triggered emergency")
        elif actual_emergency and not expected_emergency:
            results["failures"].append("FALSE_EMERGENCY: emergency triggered incorrectly")

    # 3. Top-1 accuracy
    diffs = pipeline_output.get("differential_diagnosis", [])
    top1 = diffs[0].get("disease_name", "") if diffs else ""
    top3 = [d.get("disease_name", "") for d in diffs[:3]]
    expected_top3 = case.get("expected_top_3_diagnoses", [case.get("final_diagnosis", "")])
    final_dx = case.get("final_diagnosis", "")

    if top1 == final_dx:
        results["passes"].append(f"TOP1_CORRECT: {top1}")
    elif any(dx.lower() in top1.lower() or top1.lower() in dx.lower() for dx in [final_dx]):
        results["passes"].append(f"TOP1_PARTIAL: {top1} ~ {final_dx}")
    else:
        results["failures"].append(f"TOP1_WRONG: expected={final_dx}, got={top1}")

    # 4. Top-3 accuracy
    top3_hit = any(
        any(exp.lower() in got.lower() or got.lower() in exp.lower()
            for got in top3)
        for exp in expected_top3
    )
    if top3_hit:
        results["passes"].append("TOP3_CORRECT")
    else:
        results["warnings"].append(f"TOP3_MISS: expected={expected_top3}, got={top3}")

    # 5. Hallucination check
    halluc = case.get("hallucination_check", {})
    should_not_recommend = halluc.get("should_not_recommend", [])
    meds_recommended = [
        m.get("medicine", "") for m in pipeline_output.get("recommended_medicines", [])
    ]
    meds_str = " ".join(meds_recommended).lower()
    hallucinations_found = [
        drug for drug in should_not_recommend
        if drug.lower() in meds_str
    ]
    if hallucinations_found:
        results["failures"].append(f"HALLUCINATION: {hallucinations_found}")
    else:
        results["passes"].append("NO_HALLUCINATION")

    # 6. Medicine gate check (confidence < 70% should suppress)
    if pipeline_output["confidence_score"] < 0.70:
        if pipeline_output["medicine_recommendation_suppressed"]:
            results["passes"].append("MEDICINE_GATE_CORRECT")
        else:
            results["failures"].append(
                f"MEDICINE_GATE_VIOLATION: conf={pipeline_output['confidence_score']}, "
                f"meds not suppressed"
            )

    results["all_pass"] = len(results["failures"]) == 0
    return results


def run_validation(verbose: bool = True) -> Dict[str, Any]:
    """
    Main validation runner.
    Returns a metrics summary and saves failure report.
    """
    print("\n" + "=" * 65)
    print("AuraMed AI v2.0 — Clinical Validation Suite")
    print("=" * 65)

    conn = sqlite3.connect(settings.DATABASE_PATH)
    cases = load_all_cases()

    if not cases:
        print("  [WARN] No validation cases found. Create cases in clinical_validation/*/")
        conn.close()
        return {"total": 0, "message": "No cases found"}
        
    import random
    # Fixed seed for consistent Train/Eval splits across runs
    random.seed(42)
    random.shuffle(cases)
    
    dev_split_idx = int(len(cases) * 0.70)
    dev_cases = cases[:dev_split_idx]
    eval_cases = cases[dev_split_idx:]

    print(f"  Loaded {len(cases)} total cases from {VALIDATION_DIR}")
    print(f"  [Dev Set (70%)]: {len(dev_cases)} cases")
    print(f"  [Hidden Eval Set (30%)]: {len(eval_cases)} cases")
    print("  Running pipeline on Dev Set...\n")
    
    # Run the pipeline only on the Dev set for the verbose output and main metrics
    # The eval set is evaluated at the end
    metrics = {
        "total_cases": len(dev_cases),
        "total_eval_cases": len(eval_cases),
        "triage_correct": 0,
        "top1_correct": 0,
        "top3_correct": 0,
        "emergency_correct": 0,
        "false_emergency": 0,
        "missed_emergency": 0,
        "hallucinations": 0,
        "medicine_gate_correct": 0,
        "medicine_gate_violations": 0,
        "all_pass": 0,
        "failures_by_specialty": {},
        "failure_count": 0,
    }

    all_results = []
    failure_cases = []

    for idx, case in enumerate(dev_cases):
        case_id = case.get("case_id", f"CASE_{idx}")
        specialty = case.get("specialty", "Unknown")
        final_dx = case.get("final_diagnosis", "?")

        try:
            output = run_pipeline_on_case(case, conn)
            evaluation = evaluate_case(case, output)

            if verbose:
                status = "PASS" if evaluation["all_pass"] else "FAIL"
                print(f"  {status} [{case_id}] {final_dx} | triage:{output['triage_status']} | conf:{output['confidence_score']:.0%}")
                if not evaluation["all_pass"]:
                    for f in evaluation["failures"]:
                        print(f"       FAIL: {f}")

            # Count metrics
            if any("TRIAGE_CORRECT" in p for p in evaluation["passes"]):
                metrics["triage_correct"] += 1
            if any("TOP1_CORRECT" in p or "TOP1_PARTIAL" in p for p in evaluation["passes"]):
                metrics["top1_correct"] += 1
            if any("TOP3_CORRECT" in p for p in evaluation["passes"]):
                metrics["top3_correct"] += 1
            if any("EMERGENCY_CORRECT" in p for p in evaluation["passes"]):
                metrics["emergency_correct"] += 1
            if any("FALSE_EMERGENCY" in f for f in evaluation["failures"]):
                metrics["false_emergency"] += 1
            if any("MISSED_EMERGENCY" in f for f in evaluation["failures"]):
                metrics["missed_emergency"] += 1
            if any("HALLUCINATION" in f for f in evaluation["failures"]):
                metrics["hallucinations"] += 1
            if any("MEDICINE_GATE_CORRECT" in p for p in evaluation["passes"]):
                metrics["medicine_gate_correct"] += 1
            if any("MEDICINE_GATE_VIOLATION" in f for f in evaluation["failures"]):
                metrics["medicine_gate_violations"] += 1
            if evaluation["all_pass"]:
                metrics["all_pass"] += 1
            else:
                metrics["failure_count"] += 1
                metrics["failures_by_specialty"][specialty] = (
                    metrics["failures_by_specialty"].get(specialty, 0) + 1
                )
                failure_cases.append({
                    "case_id": case_id,
                    "specialty": specialty,
                    "final_diagnosis": final_dx,
                    "failures": evaluation["failures"],
                    "warnings": evaluation["warnings"],
                    "pipeline_output": {
                        "triage": output["triage_status"],
                        "top1": (output["differential_diagnosis"] or [{}])[0].get("disease_name"),
                        "confidence": output["confidence_score"],
                        "is_emergency": output["is_emergency"],
                    },
                    "case_file": case.get("_file"),
                })

            all_results.append(evaluation)

        except Exception as e:
            print(f"  [ERROR] Case {case_id} crashed: {e}")
            failure_cases.append({
                "case_id": case_id,
                "specialty": specialty,
                "final_diagnosis": final_dx,
                "failures": [f"PIPELINE_CRASH: {str(e)}"],
                "case_file": case.get("_file"),
            })
            metrics["failure_count"] += 1

    # Calculate rates
    n = metrics["total_cases"]
    summary = {
        **metrics,
        "triage_accuracy_pct": round(metrics["triage_correct"] / n * 100, 1) if n else 0,
        "top1_accuracy_pct": round(metrics["top1_correct"] / n * 100, 1) if n else 0,
        "top3_accuracy_pct": round(metrics["top3_correct"] / n * 100, 1) if n else 0,
        "emergency_detection_pct": round(metrics["emergency_correct"] / n * 100, 1) if n else 0,
        "hallucination_rate_pct": round(metrics["hallucinations"] / n * 100, 1) if n else 0,
        "pass_rate_pct": round(metrics["all_pass"] / n * 100, 1) if n else 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Save failure report
    failure_report_path = os.path.join(
        FAILURE_DIR,
        f"failure_report_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    with open(failure_report_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": summary,
            "failures": failure_cases,
        }, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 65)
    print("VALIDATION SUMMARY (DEV SET)")
    print("=" * 65)
    print(f"  Total Cases (Dev):      {n}")
    print(f"  All-Pass Rate:          {summary['pass_rate_pct']}%")
    print(f"  Triage Accuracy:        {summary['triage_accuracy_pct']}%")
    print(f"  Top-1 Accuracy:         {summary['top1_accuracy_pct']}%")
    print(f"  Top-3 Accuracy:         {summary['top3_accuracy_pct']}%")
    print(f"  Emergency Detection:    {summary['emergency_detection_pct']}%")
    print(f"  False Emergency Rate:   {metrics['false_emergency']} cases")
    print(f"  Missed Emergency:       {metrics['missed_emergency']} cases")
    print(f"  Hallucination Rate:     {summary['hallucination_rate_pct']}%")
    print(f"  Medicine Gate Correct:  {metrics['medicine_gate_correct']}")
    print(f"  Medicine Gate Violations:{metrics['medicine_gate_violations']}")
    print(f"\n  Failures by Specialty:")
    for spec, count in sorted(metrics["failures_by_specialty"].items()):
        print(f"    {spec}: {count} failures")
    print(f"\n  Failure report saved: {failure_report_path}")
    print("=" * 65)
    
    # Run Hidden Eval
    print("\n" + "=" * 65)
    print("HIDDEN EVAL SET SUMMARY")
    print("=" * 65)
    eval_top1_correct = 0
    for case in eval_cases:
        output = run_pipeline_on_case(case, conn)
        evaluation = evaluate_case(case, output)
        if any("TOP1_CORRECT" in p or "TOP1_PARTIAL" in p for p in evaluation["passes"]):
            eval_top1_correct += 1
            
    eval_top1_pct = round((eval_top1_correct / len(eval_cases)) * 100, 1)
    print(f"  Total Cases (Hidden):   {len(eval_cases)}")
    print(f"  Hidden Top-1 Accuracy:  {eval_top1_pct}%")
    print("=" * 65 + "\n")
    
    conn.close()

    return summary

if __name__ == "__main__":
    run_validation(verbose=True)
