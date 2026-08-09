import sqlite3
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.database import get_db
from app.schemas.dosage_schema import DosageReferenceResponse
from app.services.dosage_engine import extract_dosage_reference

router = APIRouter(prefix="/dosage", tags=["Dosage Reference Engine"])

@router.get("/reference", response_model=DosageReferenceResponse)
def get_dosage_reference_by_name(
    medicine_name: str = Query(..., min_length=1, description="Medicine or active ingredient name e.g. 'Paracetamol'"),
    db: sqlite3.Connection = Depends(get_db)
):
    """
    Retrieve clinical reference dosage parameters:
    Standard Adult Dose, Pediatric Dose, Maximum Daily Dose, Route, Frequency, Duration, and Legal Disclaimer.
    """
    return extract_dosage_reference(medicine_name=medicine_name, medicine_id=None, db=db)

@router.get("/reference/{medicine_id}", response_model=DosageReferenceResponse)
def get_dosage_reference_by_id(
    medicine_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    """Lookup clinical reference dosage parameters by medicine ID."""
    return extract_dosage_reference(medicine_name="", medicine_id=medicine_id, db=db)
