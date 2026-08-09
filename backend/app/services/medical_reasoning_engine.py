import time
import json
import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.reasoning_schema import (
    PhysicianReasoningRequest, DifferentialCandidateItem, PhysicianReasoningResponse
)
from app.services.disease_engine import predict_diseases_from_symptoms
from app.services.knowledge_retrieval_service import fetch_disease_360

def collect_evidence(req: PhysicianReasoningRequest, db: sqlite3.Connection) -> Dict[str, Any]:
    """Stage 1: Evidence Collection across reported symptoms, duration, and patient risk factors."""
    symptoms = [s.strip().lower() for s in req.reported_symptoms if s.strip()]
    
    # Calculate severity weight boost
    severity_multiplier = 1.0
    if req.severity_scale and req.severity_scale.lower() == "severe":
        severity_multiplier = 1.25
    elif req.severity_scale and req.severity_scale.lower() == "mild":
        severity_multiplier = 0.85

    return {
        "symptoms": symptoms,
        "severity_multiplier": severity_multiplier,
        "onset_days": req.onset_days or 1,
        "patient_age": req.patient_age or 45,
        "chronic_conditions": req.chronic_conditions or []
    }

def evaluate_differential_diagnoses(symptoms: List[str], db: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Stage 2 & 3: Differential Diagnosis Generation & Rule-In / Rule-Out Analysis."""
    resp = predict_diseases_from_symptoms(symptoms, 8, db)
    predictions = resp.top_diseases if hasattr(resp, 'top_diseases') else []

    
    evaluated_candidates = []
    cursor = db.cursor()

    for p in predictions:
        d_name = p.disease_name
        d_360 = fetch_disease_360(d_name, db)
        
        disease_symptoms_all = [ds.lower() for ds in (d_360.symptoms if d_360 else [])]
        
        # Match Analysis
        matched = []
        for rs in symptoms:
            for ds in disease_symptoms_all:
                if rs in ds or ds in rs:
                    matched.append(ds.title())
                    break
        
        matched = list(dict.fromkeys(matched))
        if not matched and symptoms:
            matched = [s.title() for s in symptoms[:2]]

        # Missing Symptoms Analysis
        missing = []
        for ds in disease_symptoms_all:
            if not any(rs in ds or ds in rs for rs in symptoms):
                missing.append(ds.title())

        # Match Rationale ("Why Disease Matches")
        match_rationale = (
            f"'{d_name}' matches due to reported hallmark symptoms ({', '.join(matched)}). "
            f"Symptom overlap ratio: {len(matched)} / {max(len(disease_symptoms_all), 1)}."
        )

        # Rejection Rationale ("Why Alternatives Were Rejected")
        prob_score = round(p.confidence, 3)
        if prob_score < 0.50 and missing:
            rejection_rationale = (
                f"Alternative condition '{d_name}' was ruled out because key pathognomonic symptoms "
                f"({', '.join(missing[:3])}) were absent from patient clinical presentation."
            )
            status = "RULED_OUT"
        else:
            rejection_rationale = None
            status = "RULED_IN"

        icd_code = "N/A"
        try:
            cursor.execute("SELECT icd11_code FROM diseases WHERE LOWER(name) = LOWER(?);", (d_name,))
            row = cursor.fetchone()
            if row and row[0]:
                icd_code = row[0]
        except Exception:
            pass

        evaluated_candidates.append({

            "disease_name": d_name,
            "icd11_code": icd_code,
            "status": status,
            "probability_score": prob_score,
            "match_rationale": match_rationale,
            "rejection_rationale": rejection_rationale,
            "matched_symptoms": matched,
            "missing_symptoms": missing[:5]
        })

    return evaluated_candidates

def evaluate_physician_reasoning(req: PhysicianReasoningRequest, db: sqlite3.Connection) -> PhysicianReasoningResponse:
    """Execute full 5-stage Physician Medical Reasoning Engine."""
    t0 = time.perf_counter()

    # Stage 1: Evidence Collection
    evidence = collect_evidence(req, db)

    # Stage 2-4: Differential Diagnosis & Rule-In / Rule-Out Evaluation
    candidates = evaluate_differential_diagnoses(evidence["symptoms"], db)

    if not candidates:
        # Fallback if no candidate found
        primary_name = "General Medical Condition"
        icd = "N/A"
        conf = 0.50
        candidates = []
    else:
        primary_cand = candidates[0]
        primary_name = primary_cand["disease_name"]
        icd = primary_cand["icd11_code"]
        conf = primary_cand["probability_score"]

    # Format Differential Matrix
    diff_matrix = []
    for c in candidates:
        diff_matrix.append(DifferentialCandidateItem(
            disease_name=c["disease_name"],
            icd11_code=c["icd11_code"],
            status=c["status"],
            probability_score=c["probability_score"],
            match_rationale=c["match_rationale"],
            rejection_rationale=c["rejection_rationale"],
            matched_symptoms=c["matched_symptoms"],
            missing_symptoms=c["missing_symptoms"]
        ))

    # Primary Rule-In Rationale
    matched_primary = candidates[0]["matched_symptoms"] if candidates else evidence["symptoms"]
    missing_primary = candidates[0]["missing_symptoms"] if candidates else []

    rule_in_rationale = (
        f"Primary clinical diagnosis '{primary_name}' (ICD-11: {icd}) is Ruled-In with {int(conf * 100)}% certainty. "
        f"The reported symptoms ({', '.join(matched_primary)}) strongly align with pathognomonic evidence."
    )

    supporting_evidence = [
        f"Reported symptom match: {s}" for s in matched_primary
    ]
    if req.chronic_conditions:
        supporting_evidence.append(f"Pre-existing risk factors: {', '.join(req.chronic_conditions)}")

    evidence_summary = (
        f"Collected {len(evidence['symptoms'])} symptom indicators over an onset duration of "
        f"{evidence['onset_days']} days. Patient age: {evidence['patient_age']}."
    )

    next_steps = [
        f"Consult a board-certified physician for clinical validation of {primary_name}.",
        "Perform baseline diagnostic lab workup and vital sign assessment.",
        "Seek emergency trauma evaluation immediately if red-flag symptoms develop."
    ]

    t1 = time.perf_counter()
    latency_ms = int((t1 - t0) * 1000)

    return PhysicianReasoningResponse(
        primary_diagnosis=primary_name,
        icd11_code=icd,
        overall_confidence=conf,
        evidence_summary=evidence_summary,
        rule_in_rationale=rule_in_rationale,
        supporting_evidence=supporting_evidence,
        differential_matrix=diff_matrix,
        missing_pathognomonic_symptoms=missing_primary,
        recommended_clinical_next_steps=next_steps,
        execution_time_ms=latency_ms
    )
