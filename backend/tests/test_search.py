import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.database import init_user_db
from app.main import app

client = TestClient(app)

SEARCH_MED_ID = 99977

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (SEARCH_MED_ID,))
        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (99977, 'Cipla Ltd');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (?, 'Fluconazole Antifungal 150mg Test Tablet', 'Fluconazole Antifungal 150mg Test Tablet', 'Fluconazole', 'fluconazole antifungal 150mg test tablet', 45.00, 'Fluconazole (150mg)', 99977);
        """, (SEARCH_MED_ID,))
        conn.commit()
    finally:
        conn.close()

def test_hybrid_search_antifungal():
    payload = {
        "query": "antifungal medication",
        "top_k": 5
    }
    response = client.post("/api/v1/search/hybrid", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0
    assert len(data["documents"]) > 0
    
    top_doc = data["documents"][0]
    assert top_doc["rrf_score"] > 0.0
    assert top_doc["fts_rank"] is not None
    assert top_doc["vector_rank"] is not None
    assert "antifungal" in top_doc["title"].lower() or "fluconazole" in top_doc["title"].lower()

def test_hybrid_search_fever_and_headache():
    payload = {
        "query": "fever headache",
        "top_k": 5
    }
    response = client.post("/api/v1/search/hybrid", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0
    assert data["execution_time_ms"] >= 0.0
    
    # Check RRF score descending order
    rrf_scores = [doc["rrf_score"] for doc in data["documents"]]
    assert rrf_scores == sorted(rrf_scores, reverse=True)
