import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.followup_ai_schema import FollowUpAssessmentRequest, FollowUpAssessmentResponse
from app.services.followup_ai_engine import process_followup_assessment

router = APIRouter(prefix="/followup", tags=["Follow-Up AI ⭐⭐⭐⭐⭐"])

@router.post("/assess", response_model=FollowUpAssessmentResponse)
def assess_patient_followup_endpoint(req: FollowUpAssessmentRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute Clinical Follow-Up Assessment:
    Feeling better? -> Any new symptoms? -> Update assessment & triage.
    Maintains clinical continuity across patient consultations.
    """
    try:
        return process_followup_assessment(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Follow-up assessment failure: {str(e)}")
