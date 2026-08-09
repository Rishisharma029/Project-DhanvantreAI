import sqlite3
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.guideline_schema import (
    GuidelineMatchRequest, ClinicalGuidelineResponse, GuidelineReferenceItem
)
from app.services.clinical_guideline_engine import (
    match_clinical_guidelines, fetch_guidelines_by_authority
)

router = APIRouter(prefix="/guidelines", tags=["Clinical Guideline Engine ⭐⭐⭐⭐⭐"])

@router.post("/match", response_model=ClinicalGuidelineResponse)
def match_guidelines_endpoint(req: GuidelineMatchRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Match clinical condition and symptoms against official WHO, CDC, NICE, and National Guidelines.
    Every recommendation references specific guideline sections (e.g. WHO-TRS-961 Sec 4.2, NICE-NG191 Sec 1.3).
    """
    try:
        return match_clinical_guidelines(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clinical Guideline Engine failure: {str(e)}")

@router.get("/authority/{authority_code}", response_model=List[GuidelineReferenceItem])
def get_guidelines_by_authority_endpoint(authority_code: str):
    """Retrieve official guideline citations for an authority (WHO, CDC, NICE, NATIONAL_ICMR, NATIONAL_FDA)."""
    items = fetch_guidelines_by_authority(authority_code)
    if not items:
        raise HTTPException(status_code=404, detail=f"No guidelines found for authority: {authority_code}")
    return items
