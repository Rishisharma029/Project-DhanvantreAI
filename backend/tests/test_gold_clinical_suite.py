import os
import sys
import glob
import json
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.orchestrator_schema import OrchestratorRequest
from app.services.llm_orchestrator import orchestrate_llm_pipeline
from app.schemas.safety_schema import SafetyValidateRequest, PatientProfileInput
from app.services.safety_engine import validate_patient_safety
from app.config import settings

def get_db_connection():
    db_path = settings.DATABASE_PATH
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn

def load_gold_vignettes():
    dirs = [
        os.path.join(os.path.dirname(__file__), "gold_clinical_suite"),
        os.path.join(settings.ROOT_DIR, "backend", "clinical_validation")
    ]
    vignettes = []
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(".json"):
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                        vignettes.append((f, data))
    return vignettes

VIGNETTES = load_gold_vignettes()

@pytest.mark.parametrize("filename,vignette", VIGNETTES)
def test_gold_clinical_vignette(filename, vignette):
    conn = get_db_connection()
    try:
        category = vignette.get("category") or vignette.get("domain")
        
        # Test Orchestration Cases
        if category in ["respiratory", "respiratory_cases", "cardiology", "neurology", "pediatrics", "geriatrics", "dermatology", "endocrinology", "psychiatry", "emergencies", "emergency_cases", "hallucination"]:
            patient = vignette.get("patient") or vignette.get("patient_demographics", {})
            hist = vignette.get("history", {})
            symptom_list = vignette.get("symptoms", [])
            query_str = vignette.get("input_query") or f"{hist.get('chief_complaint', '')}, {', '.join(symptom_list)}"

            req = OrchestratorRequest(
                query=query_str,
                patient_age=patient.get("age", 30),
                patient_gender=patient.get("gender", "male"),
                pregnancy_status=patient.get("pregnancy_status", False),
                allergies=hist.get("allergies") or patient.get("allergies", []),
                current_medications=hist.get("current_medications") or patient.get("current_medications", []),
                turns_answered=0
            )
            res = orchestrate_llm_pipeline(req, conn)

            # Assert Triage & Emergency Rules
            if "expected_triage" in vignette:
                assert res.triage_status == vignette["expected_triage"], f"Failed triage in {filename}"
            if "expected_emergency" in vignette:
                assert res.is_emergency == vignette["expected_emergency"], f"Failed emergency detection in {filename}"

            # Assert Calibrated Confidence Range
            if "expected_confidence_range" in vignette:
                c_min, c_max = vignette["expected_confidence_range"]
                assert c_min <= res.confidence_score <= c_max, f"Confidence {res.confidence_score} outside [{c_min}, {c_max}] in {filename}"

            # Assert Top 3 Differential Candidates
            if "expected_top_3_differentials" in vignette:
                top_names = [d["disease_name"] for d in res.differential_diagnosis[:3]]
                for expected in vignette["expected_top_3_differentials"]:
                    assert any(expected.lower() in t.lower() for t in top_names), f"Missing expected differential '{expected}' in {filename}"

            # Assert Forbidden Repeated Questions
            if "forbidden_questions" in vignette:
                for forbidden in vignette["forbidden_questions"]:
                    assert not any(forbidden.lower() in q.lower() for q in res.followup_questions), f"Found forbidden question '{forbidden}' in {filename}"

        # Test Safety / Drug Interaction Cases
        elif "medicine_query" in vignette:
            patient = vignette.get("patient", {})
            prof = PatientProfileInput(
                age=patient.get("age", 30),
                gender=patient.get("gender", "female"),
                pregnancy_status=patient.get("pregnancy_status", False),
                allergies=patient.get("allergies", []),
                current_medications=patient.get("current_medications", [])
            )
            safety_req = SafetyValidateRequest(
                medicine_name=vignette["medicine_query"],
                patient_profile=prof
            )
            s_res = validate_patient_safety(safety_req, conn)

            if "expected_safety_grade" in vignette:
                assert s_res.safety_grade == vignette["expected_safety_grade"], f"Safety grade mismatch in {filename}"
            if "expected_warnings_contain" in vignette:
                w_target = vignette["expected_warnings_contain"].lower()
                all_warns = " ".join([w.message.lower() for w in s_res.warnings])
                assert w_target in all_warns, f"Missing warning keyword '{w_target}' in {filename}"

    finally:
        conn.close()
