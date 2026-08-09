import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.database import init_user_db
from app.main import app
from app.services.audit_service import log_system_audit_event, log_recommendation_history_event

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    try:
        log_system_audit_event(1, "AI_CALL", "/api/v1/orchestrator/query", "POST", 200, 340, "LLM query executed", '{"tools":["symptom_search"]}', conn)
        log_system_audit_event(1, "ERROR", "/api/v1/medicine/invalid", "GET", 404, 12, "Medicine not found", '{}', conn)
        log_system_audit_event(1, "SEARCH_QUERY", "/api/v1/search/universal", "GET", 200, 45, "Search executed", '{"q":"Paracetamol"}', conn)
        log_recommendation_history_event(
            user_id=1,
            session_id="sess-999",
            symptoms=["fever", "headache"],
            diseases=[{"name": "Viral Fever", "confidence": 0.88}],
            medicines=[{"name": "Paracetamol 650mg"}],
            warnings=["Do not exceed 4000mg/day"],
            db=conn
        )
    finally:
        conn.close()

def test_api_requests_audit():
    # Execute endpoint to trigger middleware
    client.get("/health")
    response = client.get("/api/v1/audit/api-requests")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_ai_calls_audit():
    response = client.get("/api/v1/audit/ai-calls")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["log_type"] == "AI_CALL"

def test_errors_audit():
    response = client.get("/api/v1/audit/errors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_searches_audit():
    response = client.get("/api/v1/audit/searches")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_recommendations_audit():
    response = client.get("/api/v1/audit/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "Viral Fever" in data[0]["disease_recommendations_json"]

def test_audit_summary_metrics():
    response = client.get("/api/v1/audit/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_ai_calls"] >= 1
    assert data["total_recommendations_archived"] >= 1
