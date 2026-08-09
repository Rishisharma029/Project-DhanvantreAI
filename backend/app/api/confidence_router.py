import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.confidence_schema import (
    ConfidenceCalibrateRequest, ConfidenceCalibrateResponse
)
from app.services.confidence_calibration_engine import calibrate_confidence_score

router = APIRouter(prefix="/confidence", tags=["Confidence Calibration Engine"])

@router.post("/calibrate", response_model=ConfidenceCalibrateResponse)
def calibrate_confidence_endpoint(req: ConfidenceCalibrateRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute Confidence Calibration Pipeline:
    Combines Disease Model Probability (40%), Symptom Coverage (40%), Drug Interaction Penalties, and Contradiction Safety Penalties.
    Returns calibrated Final Confidence Score (0.0 to 1.0) and Signal Breakdown.
    """
    return calibrate_confidence_score(req, db)
