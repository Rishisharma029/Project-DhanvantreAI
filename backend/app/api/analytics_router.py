import sqlite3
from typing import List, Dict
from fastapi import APIRouter, Depends, Query
from app.database import get_db
from app.schemas.analytics_schema import (
    TopSearchedItem, SearchTrendPoint, AIUsageStatistics, AnalyticsDashboardResponse
)
from app.services.analytics_engine import (
    get_top_searched_medicines, get_top_searched_diseases,
    get_search_volume_trends, get_ai_usage_statistics,
    get_analytics_dashboard_overview
)

router = APIRouter(prefix="/analytics", tags=["Analytics Engine"])

@router.get("/top-medicines", response_model=List[TopSearchedItem])
def get_top_medicines_endpoint(limit: int = Query(10, ge=1, le=50), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve most searched medicines and active ingredients."""
    return get_top_searched_medicines(limit, db)

@router.get("/top-diseases", response_model=List[TopSearchedItem])
def get_top_diseases_endpoint(limit: int = Query(10, ge=1, le=50), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve most searched diseases and differential diagnoses."""
    return get_top_searched_diseases(limit, db)

@router.get("/search-trends", response_model=List[SearchTrendPoint])
def get_search_trends_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """Retrieve search volume trends over time."""
    return get_search_volume_trends(db)

@router.get("/ai-stats", response_model=AIUsageStatistics)
def get_ai_stats_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """Retrieve AI usage statistics (total calls, avg latency, safety score, emergency rate)."""
    return get_ai_usage_statistics(db)

@router.get("/dashboard", response_model=AnalyticsDashboardResponse)
def get_analytics_dashboard_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """Retrieve unified executive Analytics Dashboard covering all 4 telemetry domains."""
    return get_analytics_dashboard_overview(db)
