import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.database import init_user_db
from app.main import app
from app.services.analytics_engine import log_search_query_event, log_ai_usage_event

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    try:
        log_search_query_event(1, "Paracetamol 650mg", "medicines", 12, conn)
        log_search_query_event(1, "Dengue Fever", "diseases", 5, conn)
        log_ai_usage_event("sess-123", 1, "I have high fever", 4, 280, False, 100.0, conn)
        log_ai_usage_event("sess-124", 1, "Chest pain emergency", 5, 410, True, 85.0, conn)
    finally:
        conn.close()

def test_top_medicines_analytics():
    response = client.get("/api/v1/analytics/top-medicines")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_top_diseases_analytics():
    response = client.get("/api/v1/analytics/top-diseases")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_search_trends_analytics():
    response = client.get("/api/v1/analytics/search-trends")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_ai_stats_analytics():
    response = client.get("/api/v1/analytics/ai-stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_ai_queries"] >= 2
    assert "emergency_rate_percentage" in data

def test_analytics_dashboard_overview():
    response = client.get("/api/v1/analytics/dashboard")
    assert response.status_code == 200
    data = response.json()

    assert data["total_search_volume"] >= 1
    assert len(data["top_medicines"]) >= 1
    assert len(data["top_diseases"]) >= 1
    assert len(data["search_trends"]) >= 1
    assert "ai_usage_statistics" in data
