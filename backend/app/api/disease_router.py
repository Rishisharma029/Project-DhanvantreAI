import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.disease_schema import (
    DiseasePredictRequest, DiseasePredictResponse
)
from app.services.disease_engine import predict_diseases_from_symptoms

router = APIRouter(prefix="/disease-prediction", tags=["Disease Prediction Engine ⭐⭐⭐⭐⭐"])

@router.post("/predict", response_model=DiseasePredictResponse)
def predict_disease(body: DiseasePredictRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Predict top candidate diseases based on input symptoms:
    - Calculates diagnostic confidence percentage
    - Classifies disease severity (Emergency, Severe, Moderate, Mild)
    - Returns matching symptoms supporting diagnosis
    - Returns missing symptoms needed for differential diagnosis
    - Returns clinical precautions
    """
    return predict_diseases_from_symptoms(body.symptoms, body.top_n or 5, db)
