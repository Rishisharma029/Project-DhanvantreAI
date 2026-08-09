import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.explainability_schema import (
    ExplainabilityRequest, ExplainabilityResponse
)
from app.services.explainability_engine import generate_clinical_explanation

router = APIRouter(prefix="/explainability", tags=["Explainability Engine"])

@router.post("/explain", response_model=ExplainabilityResponse)
def explainability_endpoint(req: ExplainabilityRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Generate 5-Pillar Clinical Explainability Report:
    - Why Disease? (Symptom evidence & disease presentation)
    - Why Medicine? (Therapeutic indication & safety rationale)
    - Why Confidence? (Sensitivity, precision, and formula breakdown)
    - Alternative Diseases (Differential diagnoses & overlapping symptoms)
    - Missing Symptoms (Unreported symptoms & rule-out rationale)
    """
    return generate_clinical_explanation(req, db)
