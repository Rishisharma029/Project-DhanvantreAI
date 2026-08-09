import sqlite3
from typing import List
from fastapi import APIRouter, Depends, Query
from app.database import get_db
from app.schemas.audit_schema import (
    AuditLogItem, RecommendationHistoryItem, AuditSummaryResponse
)
from app.services.audit_service import (
    get_audit_logs_by_type, get_recommendation_history, get_audit_summary_metrics
)

router = APIRouter(prefix="/audit", tags=["Logging & Audit Engine"])

@router.get("/api-requests", response_model=List[AuditLogItem])
def get_api_requests_audit(limit: int = Query(50, ge=1, le=200), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve API Request audit logs."""
    return get_audit_logs_by_type("API_REQUEST", limit, db)

@router.get("/ai-calls", response_model=List[AuditLogItem])
def get_ai_calls_audit(limit: int = Query(50, ge=1, le=200), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve AI Call audit logs."""
    return get_audit_logs_by_type("AI_CALL", limit, db)

@router.get("/errors", response_model=List[AuditLogItem])
def get_errors_audit(limit: int = Query(50, ge=1, le=200), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve Error & Exception audit logs."""
    return get_audit_logs_by_type("ERROR", limit, db)

@router.get("/searches", response_model=List[AuditLogItem])
def get_searches_audit(limit: int = Query(50, ge=1, le=200), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve Search Query audit logs."""
    return get_audit_logs_by_type("SEARCH_QUERY", limit, db)

@router.get("/recommendations", response_model=List[RecommendationHistoryItem])
def get_recommendations_audit(user_id: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve Recommendation History audit logs."""
    return get_recommendation_history(user_id, limit, db)

@router.get("/summary", response_model=AuditSummaryResponse)
def get_audit_summary_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """Retrieve unified summary metrics across all 5 audit streams."""
    return get_audit_summary_metrics(db)
