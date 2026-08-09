import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.med_safety_schema import MedicationSafetyRequest, MedicationSafetyResponse
from app.services.medication_safety_ai import evaluate_medication_safety

router = APIRouter(prefix="/med-safety", tags=["Medication Safety AI ⭐⭐⭐⭐⭐"])

@router.post("/evaluate", response_model=MedicationSafetyResponse)
def evaluate_medication_safety_endpoint(req: MedicationSafetyRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 10-Point Advanced Clinical Medication Safety Audit:
    Evaluates Pregnancy, Lactation, Pediatrics, Geriatrics (Beers Criteria), Renal adjustment, Hepatic adjustment, Allergy cross-reactivity, QT prolongation, Duplicate therapy, and Black box warnings.
    Produces Safety Score (0-100), Risk Level, and Actionable Recommendations.
    """
    try:
        return evaluate_medication_safety(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Medication Safety AI failure: {str(e)}")
