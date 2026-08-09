import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.hallucination_guard_schema import HallucinationGuardRequest, HallucinationGuardResponse
from app.services.hallucination_guard_engine import evaluate_hallucination_guard

router = APIRouter(prefix="/hallucination-guard", tags=["AI Hallucination Guard ⭐⭐⭐⭐⭐"])

@router.post("/audit", response_model=HallucinationGuardResponse)
def audit_llm_hallucinations(req: HallucinationGuardRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    AI Hallucination Guard Pre-Response Verification:
    LLM -> Claim Extraction -> Evidence Verification -> Mismatch Detection -> Auto-Regeneration & Sanitization.
    Ensures zero unsupported medical claims reach the user.
    """
    try:
        return evaluate_hallucination_guard(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hallucination Guard execution failure: {str(e)}")
