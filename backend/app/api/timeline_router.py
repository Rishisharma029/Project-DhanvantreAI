import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.clinical_timeline_schema import ClinicalTimelineRequest, ClinicalTimelineResponse
from app.services.clinical_timeline_engine import generate_clinical_timeline

router = APIRouter(prefix="/timeline", tags=["Clinical Timeline Engine ⭐⭐⭐⭐⭐"])

@router.post("/generate", response_model=ClinicalTimelineResponse)
def generate_clinical_timeline_endpoint(req: ClinicalTimelineRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Generate 5-Stage Visual Clinical Timeline:
    1. Symptoms (Onset & Evolution)
    2. Assessment (Diagnostic Triage & Labs)
    3. Medicines (Pharmacotherapy & Regimen)
    4. Follow-up (Clinical Review & Re-eval)
    5. Recovery (Convalescence & Full Functional Return)
    """
    try:
        return generate_clinical_timeline(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clinical Timeline Engine failure: {str(e)}")
