import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.safety_schema import (
    SafetyValidateRequest, SafetyValidateResponse
)
from app.services.safety_engine import validate_patient_safety

router = APIRouter(prefix="/safety", tags=["Safety Validation Engine ⭐⭐⭐⭐⭐"])

@router.post("/validate", response_model=SafetyValidateResponse)
def validate_safety_endpoint(body: SafetyValidateRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 9 Clinical Safety Audits:
    Allergies, Pregnancy, Age, Pediatric, Geriatric, Kidney Disease, Liver Disease, Contraindications, Drug Interactions.
    Produces Safety Score (0-100%), Safety Grade (SAFE, CAUTION, UNSAFE, CONTRAINDICATED), and Warnings list.
    """
    return validate_patient_safety(body, db)
