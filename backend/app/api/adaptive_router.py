import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.adaptive_schema import (
    AdaptiveEvaluationRequest, AdaptiveEvaluationResponse, AdaptiveEngineJSONResponse
)
from app.services.adaptive_engine import evaluate_adaptive_questioning, evaluate_adaptive_clinical_questioning

router = APIRouter(prefix="/adaptive-questions", tags=["Adaptive Question Engine ⭐⭐⭐⭐⭐"])

@router.post("/evaluate", response_model=AdaptiveEvaluationResponse)
def evaluate_question_engine(req: AdaptiveEvaluationRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Evaluate consultation state:
    - Emergency red-flag detection
    - Diagnostic confidence calculation
    - Information gain question generation
    - Termination checks (Confidence threshold >= 85%, Max limit = 5)
    """
    return evaluate_adaptive_questioning(req, db)

@router.post("/evaluate-json", response_model=AdaptiveEngineJSONResponse)
def evaluate_question_engine_json(req: AdaptiveEvaluationRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Evaluates consultation state using AuraMed AI's 10-Step Adaptive Specification
    Returns strict structured JSON format.
    """
    return evaluate_adaptive_clinical_questioning(req, db)
