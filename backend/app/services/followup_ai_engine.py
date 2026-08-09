import uuid
import sqlite3
from app.schemas.followup_ai_schema import (
    FollowUpAssessmentRequest,
    FollowUpAssessmentResponse,
    SymptomProgressionStatus
)

def process_followup_assessment(req: FollowUpAssessmentRequest, db: sqlite3.Connection) -> FollowUpAssessmentResponse:
    """
    Execute Clinical Follow-Up Loop:
    Feeling better? -> Any new symptoms? -> Update assessment & clinical triage.
    """
    new_syms = req.new_symptoms or []
    res_syms = req.resolved_symptoms or []

    # Determine progression status
    if req.feeling_better and len(new_syms) == 0:
        if len(res_syms) > 0:
            status = SymptomProgressionStatus.RESOLVED if "all" in [s.lower() for s in res_syms] else SymptomProgressionStatus.IMPROVING
        else:
            status = SymptomProgressionStatus.IMPROVING
        risk_level = "LOW_GREEN"
        assessment_update = "Symptom trajectory is favorably improving. Continue current supportive/medication regimen until completion."
        recommended_actions = [
            "Complete remaining course of prescribed medications.",
            "Maintain adequate rest and fluid hydration.",
            "Schedule routine 7-day follow-up if mild symptoms linger."
        ]
        next_days = 7

    elif not req.feeling_better or len(new_syms) > 0:
        status = SymptomProgressionStatus.WORSENING if len(new_syms) >= 2 else SymptomProgressionStatus.STABLE
        risk_level = "HIGH_ORANGE" if len(new_syms) >= 2 else "MODERATE_YELLOW"
        assessment_update = f"Reported new/persistent symptoms: {', '.join(new_syms) if new_syms else 'persistent illness'}. Recalibrating differential diagnosis and clinical triage."
        recommended_actions = [
            "Schedule an in-person physician re-evaluation within 24-48 hours.",
            "Re-assess vital signs (temperature, pulse, blood pressure).",
            "Evaluate for secondary bacterial infection or adverse drug reaction."
        ]
        next_days = 2

    else:
        status = SymptomProgressionStatus.STABLE
        risk_level = "MODERATE_YELLOW"
        assessment_update = "Symptoms remain stable without significant progression or resolution."
        recommended_actions = [
            "Continue prescribed therapy for an additional 48 hours.",
            "Monitor for high fever or respiratory distress."
        ]
        next_days = 3

    return FollowUpAssessmentResponse(
        followup_id=f"FOL-{uuid.uuid4().hex[:8].upper()}",
        progression_status=status,
        updated_risk_level=risk_level,
        clinical_assessment_update=assessment_update,
        recommended_actions=recommended_actions,
        next_followup_days=next_days
    )
