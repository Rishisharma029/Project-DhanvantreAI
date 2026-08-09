import sqlite3
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.database import get_db
from app.schemas.symptom_schema import (
    SymptomProcessRequest, SymptomProcessResponse, SymptomSearchResponse
)
from app.services.symptom_engine import (
    extract_and_normalize_symptoms, find_candidate_diseases
)

router = APIRouter(prefix="/symptoms", tags=["Symptom Processing Engine"])

@router.post("/process", response_model=SymptomProcessResponse)
def process_symptoms(body: SymptomProcessRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Process free-form natural language text to extract, normalize, resolve synonyms,
    detect severity, remove duplicates, and match candidate diseases.
    """
    extracted = extract_and_normalize_symptoms(body.text, db)
    canon_names = [s.canonical_name for s in extracted]

    # Calculate overall query severity
    overall_sev = "Moderate"
    if any(s.severity == "Emergency" for s in extracted):
        overall_sev = "Emergency"
    elif any(s.severity == "Severe" for s in extracted):
        overall_sev = "Severe"
    elif all(s.severity == "Mild" for s in extracted) and extracted:
        overall_sev = "Mild"

    candidate_diseases = find_candidate_diseases(canon_names, db)

    return SymptomProcessResponse(
        input_text=body.text,
        extracted_symptoms=extracted,
        canonical_symptom_names=canon_names,
        overall_severity=overall_sev,
        candidate_diseases=candidate_diseases
    )

@router.get("/search", response_model=list[SymptomSearchResponse])
def search_symptoms(q: str = Query(..., min_length=1), db: sqlite3.Connection = Depends(get_db)):
    """Search canonical symptoms in database with autocompletion."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, severity_weight
        FROM symptoms
        WHERE name LIKE ?
        ORDER BY severity_weight DESC, name ASC
        LIMIT 10;
    """, (f"%{q}%",))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
