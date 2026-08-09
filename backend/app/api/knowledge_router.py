import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.knowledge_schema import (
    Disease360KnowledgeResponse, Medicine360KnowledgeResponse,
    DietItem, PrecautionItem, WorkoutItem
)
from app.services.knowledge_retrieval_service import (
    fetch_disease_360, fetch_medicine_360,
    fetch_diets_by_disease, fetch_precautions_by_disease, fetch_workouts_by_disease
)

router = APIRouter(prefix="/knowledge", tags=["Knowledge Retrieval Service (Central Data Layer)"])

@router.get("/disease/{identifier}", response_model=Disease360KnowledgeResponse)
def get_disease_360_endpoint(identifier: str, db: sqlite3.Connection = Depends(get_db)):
    """Fetch 360° Knowledge Profile for a Disease (Symptoms, Diets, Precautions, Workouts)."""
    data = fetch_disease_360(identifier, db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disease knowledge record not found")
    return data

@router.get("/medicine/{identifier}", response_model=Medicine360KnowledgeResponse)
def get_medicine_360_endpoint(identifier: str, db: sqlite3.Connection = Depends(get_db)):
    """Fetch 360° Knowledge Profile for a Medicine (Ingredients, Side Effects, Interactions, Uses, Substitutes)."""
    data = fetch_medicine_360(identifier, db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine knowledge record not found")
    return data

@router.get("/diets/{disease_name}", response_model=list[DietItem])
def get_diets_endpoint(disease_name: str, db: sqlite3.Connection = Depends(get_db)):
    """Retrieve recommended dietary guidelines for a specific disease."""
    return fetch_diets_by_disease(disease_name, db)

@router.get("/precautions/{disease_name}", response_model=list[PrecautionItem])
def get_precautions_endpoint(disease_name: str, db: sqlite3.Connection = Depends(get_db)):
    """Retrieve clinical precautions for a specific disease."""
    return fetch_precautions_by_disease(disease_name, db)

@router.get("/workouts/{disease_name}", response_model=list[WorkoutItem])
def get_workouts_endpoint(disease_name: str, db: sqlite3.Connection = Depends(get_db)):
    """Retrieve recommended exercises and workouts for a specific disease."""
    return fetch_workouts_by_disease(disease_name, db)
