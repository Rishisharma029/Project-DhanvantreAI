import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.reasoning_schema import PhysicianReasoningRequest, PhysicianReasoningResponse
from app.services.medical_reasoning_engine import evaluate_physician_reasoning

router = APIRouter(prefix="/reasoning", tags=["Medical Reasoning Engine ⭐⭐⭐⭐⭐"])

@router.post("/evaluate", response_model=PhysicianReasoningResponse)
def evaluate_physician_reasoning_endpoint(req: PhysicianReasoningRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 5-Stage Physician Medical Reasoning Engine:
    Evidence Collection -> Differential Diagnosis -> Rule-In -> Rule-Out -> Final Ranking with Match/Rejection Rationales.
    """
    try:
        return evaluate_physician_reasoning(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Medical Reasoning Engine failure: {str(e)}")

@router.post("/differential-matrix")
def get_differential_matrix_endpoint(req: PhysicianReasoningRequest, db: sqlite3.Connection = Depends(get_db)):
    """Inspect full differential diagnostic matrix with Rule-In and Rule-Out rationales."""
    res = evaluate_physician_reasoning(req, db)
    return {
        "primary_diagnosis": res.primary_diagnosis,
        "overall_confidence": res.overall_confidence,
        "differential_matrix": res.differential_matrix,
        "execution_time_ms": res.execution_time_ms
    }
