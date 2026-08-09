import time
import sqlite3
from typing import List, Dict, Any
from app.schemas.differential_schema import (
    DifferentialDiagnosisRequest, DifferentialCandidateDetail, DifferentialDiagnosisResponse
)
from app.services.disease_engine import predict_diseases_from_symptoms
from app.services.knowledge_retrieval_service import fetch_disease_360

def map_severity_level(disease_name: str, confidence: float) -> str:
    """Classify clinical severity based on condition indicators and probability."""
    d_lower = disease_name.lower()
    
    if any(k in d_lower for k in ["coronary", "infarction", "stroke", "sepsis", "embolism", "acute"]):
        return "RED_EMERGENCY"
    elif any(k in d_lower for k in ["pneumonia", "covid", "influenza", "appendicitis", "asthma"]):
        return "HIGH_URGENT" if confidence >= 0.70 else "MODERATE"
    elif any(k in d_lower for k in ["viral fever", "bronchitis", "sinusitis", "gastritis"]):
        return "MODERATE"
    
    return "LOW_MILD"

def generate_differential_diagnosis(req: DifferentialDiagnosisRequest, db: sqlite3.Connection) -> DifferentialDiagnosisResponse:
    """Execute Multi-Candidate Differential Diagnosis Evaluation."""
    t0 = time.perf_counter()
    clean_symptoms = [s.strip().lower() for s in req.symptoms if s.strip()]

    # Predict top candidates
    resp = predict_diseases_from_symptoms(clean_symptoms, 6, db)
    predictions = resp.top_diseases if hasattr(resp, 'top_diseases') else []

    
    candidates = []
    for idx, p in enumerate(predictions, start=1):
        d_name = p.disease_name
        d_360 = fetch_disease_360(d_name, db)
        
        disease_symptoms_all = [ds.lower() for ds in (d_360.symptoms if d_360 else [])]
        
        # Evidence (Supporting Clinical Findings)
        evidence = []
        for rs in clean_symptoms:
            for ds in disease_symptoms_all:
                if rs in ds or ds in rs:
                    evidence.append(f"Reported symptom match: '{ds.title()}'")
                    break

        evidence = list(dict.fromkeys(evidence))
        if not evidence and clean_symptoms:
            evidence = [f"Clinical symptom indicator: '{s.title()}'" for s in clean_symptoms]

        # Missing Findings (Pathognomonic Symptoms Absent)
        missing_findings = []
        for ds in disease_symptoms_all:
            if not any(rs in ds or ds in rs for rs in clean_symptoms):
                missing_findings.append(f"Unreported hallmark symptom: '{ds.title()}'")

        prob_val = min(round(p.confidence, 2), 0.99)
        prob_pct = f"{int(prob_val * 100)}%"
        severity = map_severity_level(d_name, prob_val)
        
        # Safely fetch ICD-11 code from DB
        icd_code = "N/A"
        try:
            cursor = db.cursor()
            cursor.execute("SELECT icd11_code FROM diseases WHERE LOWER(name) = LOWER(?);", (d_name,))
            row = cursor.fetchone()
            if row and row[0]:
                icd_code = row[0]
        except Exception:
            pass

        rec = f"Primary diagnostic protocol for {d_name} (ICD-11: {icd_code}). Consult a physician for confirmation."


        candidates.append(DifferentialCandidateDetail(
            rank=idx,
            condition_name=d_name,
            icd11_code=icd_code,
            probability_percentage=prob_pct,
            probability_score=prob_val,
            severity_level=severity,
            evidence=evidence,
            missing_findings=missing_findings[:4],
            clinical_recommendation=rec
        ))

    t1 = time.perf_counter()
    latency_ms = int((t1 - t0) * 1000)

    return DifferentialDiagnosisResponse(
        reported_symptoms=clean_symptoms,
        total_candidates_evaluated=len(candidates),
        differential_candidates=candidates,
        execution_time_ms=latency_ms
    )
