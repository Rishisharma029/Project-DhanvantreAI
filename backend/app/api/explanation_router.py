import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.explanation_schema import ExplanationRequest, DualExplanationResponse
from app.services.dual_explanation_engine import run_dual_explanation_engine

router = APIRouter(prefix="/explanation", tags=["Dual-Mode AI Explanation Engine ⭐⭐⭐⭐⭐"])

@router.post("/generate", response_model=DualExplanationResponse)
def generate_dual_explanation_endpoint(req: ExplanationRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Generate Dual-Level AI Explanations:
    - Patient Mode: Simple, layperson English without medical jargon.
    - Professional Mode: Precise clinical terminology, Mechanism of Action (MOA), evidence citations, and contraindications.
    """
    try:
        return run_dual_explanation_engine(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dual Explanation Engine failure: {str(e)}")
