import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db
from app.services.feedback_improvement_engine import submit_ai_feedback, get_feedback_analytics
from app.schemas.feedback_improvement_schema import (
    FeedbackSubmissionRequest,
    FeedbackType,
    ReportedCategory
)

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ai_feedback_logs;")
    conn.commit()
    conn.close()

def test_submit_incorrect_suggestion_feedback():
    """Verify logging of incorrect suggestion feedback triggers prompt tuning action."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = FeedbackSubmissionRequest(
        feedback_type=FeedbackType.INCORRECT_SUGGESTION,
        query_or_context="Paracetamol dosage for toddler",
        ai_response="Give 1000mg Paracetamol",
        user_comment="Too high for a toddler",
        reported_category=ReportedCategory.WRONG_DOSAGE,
        suggested_correction="Pediatric dosing is 10-15mg/kg"
    )
    res = submit_ai_feedback(req, conn)
    conn.close()

    assert res.feedback_id.startswith("FB-")
    assert res.status == "PROMPT_OPTIMIZED"
    assert "PROMPT_TUNING_TRIGGERED" in res.continuous_improvement_action

def test_submit_missing_data_feedback():
    """Verify missing data reports trigger RAG vector re-indexing."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = FeedbackSubmissionRequest(
        feedback_type=FeedbackType.MISSING_DATA,
        query_or_context="Treatment for rare tropical disease X",
        ai_response="No information available",
        user_comment="Disease X is missing from knowledge base",
        reported_category=ReportedCategory.MISSING_DRUG
    )
    res = submit_ai_feedback(req, conn)
    conn.close()

    assert res.status == "RETRIEVAL_INDEXED"
    assert "KNOWLEDGE_GRAPH_EXPANSION" in res.continuous_improvement_action

def test_feedback_analytics_and_api():
    """Test REST API endpoints POST /api/v1/feedback/submit and GET /api/v1/feedback/analytics."""
    # 1. Submit rating feedback
    payload = {
        "feedback_type": "RATING",
        "rating": 5,
        "query_or_context": "What are side effects of Paracetamol?",
        "ai_response": "Nausea, rash, rare hepatotoxicity in overdose.",
        "user_comment": "Excellent answer!"
    }
    sub_res = client.post(f"{settings.API_V1_STR}/feedback/submit", json=payload)
    assert sub_res.status_code == 200
    data = sub_res.json()
    assert "feedback_id" in data

    # 2. Get Analytics
    ana_res = client.get(f"{settings.API_V1_STR}/feedback/analytics")
    assert ana_res.status_code == 200
    a_data = ana_res.json()
    assert a_data["total_feedback_count"] >= 1
    assert a_data["average_rating"] == 5.0
