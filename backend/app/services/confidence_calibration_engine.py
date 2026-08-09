import sqlite3
from typing import Dict, Any
from app.schemas.confidence_schema import (
    ConfidenceCalibrateRequest, ConfidenceCalibrateResponse, ConfidenceSignalBreakdown
)

def calibrate_confidence_score(req: ConfidenceCalibrateRequest, db: sqlite3.Connection = None) -> ConfidenceCalibrateResponse:
    """
    Executes Confidence Calibration Engine Pipeline:
    1. Disease Model Probability (50% weight)
    2. Symptom Coverage Ratio (50% weight)
    3. Interaction Risk Penalty (-0.05 to -0.30)
    4. Contradictions & Safety Penalty (-0.10 to -0.50)
    5. High Alignment Bonus (+0.05)
    Calculates final calibrated score (0.0 to 1.0) and assigns Confidence Grade.
    """
    base_score = max(0.0, min(1.0, req.base_disease_confidence))
    disease_weighted = round(base_score * 0.50, 3)

    coverage_ratio = round(min(req.matched_symptoms_count / max(req.total_disease_symptoms_count, 1), 1.0), 3)
    coverage_weighted = round(coverage_ratio * 0.50, 3)

    # 3. Interaction Risk Penalty
    inter_sev = (req.interaction_severity or "None").lower()
    inter_penalty = 0.0
    if "major" in inter_sev:
        inter_penalty = 0.30
    elif "moderate" in inter_sev:
        inter_penalty = 0.15
    elif "minor" in inter_sev:
        inter_penalty = 0.05

    # 4. Contradiction & Safety Penalty
    s_grade = (req.safety_grade or "SAFE").upper()
    contra_penalty = 0.0
    if "CONTRAINDICATED" in s_grade:
        contra_penalty = 0.50
    elif "UNSAFE" in s_grade:
        contra_penalty = 0.30
    elif "CAUTION" in s_grade:
        contra_penalty = 0.10

    # 5. High Alignment Bonus
    s_score = req.safety_score if req.safety_score is not None else 100.0
    bonus = 0.0
    if coverage_ratio >= 0.80 and s_score >= 90.0 and contra_penalty == 0.0:
        bonus = 0.05

    # Compute raw & clamped final score
    raw_final = (disease_weighted + coverage_weighted + bonus) - (inter_penalty + contra_penalty)
    final_score = round(max(0.0, min(1.0, raw_final)), 2)
    final_pct = f"{int(final_score * 100)}%"

    # Grade assignment
    if final_score >= 0.80:
        grade = "High Confidence"
    elif final_score >= 0.60:
        grade = "Moderate Confidence"
    else:
        grade = "Low Confidence"

    breakdown = ConfidenceSignalBreakdown(
        disease_model_score=base_score,
        disease_model_weighted=disease_weighted,
        symptom_coverage_ratio=coverage_ratio,
        symptom_coverage_weighted=coverage_weighted,
        interaction_penalty=round(inter_penalty, 3),
        contradiction_penalty=round(contra_penalty, 3),
        high_alignment_bonus=round(bonus, 3)
    )

    return ConfidenceCalibrateResponse(
        disease_name=req.disease_name,
        final_confidence_score=final_score,
        final_confidence_percentage=final_pct,
        confidence_grade=grade,
        signal_breakdown=breakdown
    )
