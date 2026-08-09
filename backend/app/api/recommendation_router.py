import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.recommendation_schema import (
    RecommendationRequest, RecommendationResponse
)
from app.services.recommendation_engine import execute_recommendation_pipeline

router = APIRouter(prefix="/recommendations", tags=["Recommendation Engine ⭐⭐⭐⭐⭐"])

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(body: RecommendationRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 5-Step Recommendation Pipeline:
    Disease -> Retrieve Medicines -> Rank Medicines -> Find Alternatives -> Generate JSON
    """
    return execute_recommendation_pipeline(body.disease, body.max_recommendations or 5, db)
