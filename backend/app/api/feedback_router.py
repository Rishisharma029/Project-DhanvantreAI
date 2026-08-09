import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.feedback_improvement_schema import (
    FeedbackSubmissionRequest,
    FeedbackSubmissionResponse,
    FeedbackAnalyticsSummary
)
from app.services.feedback_improvement_engine import (
    submit_ai_feedback,
    get_feedback_analytics
)

router = APIRouter(prefix="/feedback", tags=["AI Feedback & Continuous Improvement ⭐⭐⭐⭐⭐"])

@router.post("/submit", response_model=FeedbackSubmissionResponse)
def submit_feedback_endpoint(req: FeedbackSubmissionRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Collect AI Feedback (User Ratings, Incorrect Suggestions, Missing Data Reports):
    Triggers automated continuous improvement (prompt optimization, RAG re-indexing, diagnostic recalibration).
    """
    try:
        return submit_ai_feedback(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failure: {str(e)}")

@router.get("/analytics", response_model=FeedbackAnalyticsSummary)
def get_feedback_analytics_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """Retrieve system-wide AI Feedback analytics, user ratings, and continuous improvement metrics."""
    try:
        return get_feedback_analytics(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failure: {str(e)}")
