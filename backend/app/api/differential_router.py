import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.differential_schema import DifferentialDiagnosisRequest, DifferentialDiagnosisResponse
from app.services.differential_diagnosis_engine import generate_differential_diagnosis

router = APIRouter(prefix="/differential", tags=["Differential Diagnosis Engine ⭐⭐⭐⭐⭐"])

@router.post("/diagnose", response_model=DifferentialDiagnosisResponse)
def diagnose_differential_multi(req: DifferentialDiagnosisRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Generate Multi-Candidate Differential Diagnosis List:
    Outputs ranked candidates (e.g. 1. Influenza 91%, 2. COVID 82%, 3. Viral Fever 75%, 4. Pneumonia 61%),
    each with Evidence, Missing Findings, and Severity classification.
    """
    try:
        return generate_differential_diagnosis(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Differential Diagnosis Engine failure: {str(e)}")
