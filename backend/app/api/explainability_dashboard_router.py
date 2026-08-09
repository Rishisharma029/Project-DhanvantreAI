import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.explainability_dashboard_schema import ExplainabilityDashboardRequest, ExplainabilityDashboardResponse
from app.services.explainability_dashboard_engine import generate_explainability_dashboard

router = APIRouter(prefix="/explainability", tags=["Explainability Dashboard ⭐⭐⭐⭐⭐"])

@router.post("/dashboard", response_model=ExplainabilityDashboardResponse)
def generate_explainability_dashboard_endpoint(req: ExplainabilityDashboardRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Generate 7-Step End-to-End Clinical Explainability & Transparency Trajectory:
    Symptoms -> Disease -> Confidence -> Evidence -> Medicines -> Safety -> Final Explanation.
    Provides complete clinical transparency for physicians and patients.
    """
    try:
        return generate_explainability_dashboard(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explainability Dashboard generation failure: {str(e)}")
