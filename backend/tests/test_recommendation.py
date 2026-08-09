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

REC_MED_ID = 88991

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM substitutes WHERE medicine_id = ?;", (REC_MED_ID,))
        cursor.execute("DELETE FROM medicine_uses WHERE medicine_id = ?;", (REC_MED_ID,))
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (REC_MED_ID,))

        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (88991, 'Cipla Ltd');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id, is_discontinued)
            VALUES (?, 'Fluconazole 150mg Test Tablet', 'Fluconazole 150mg Test Tablet', 'Fluconazole', 'fluconazole 150mg test tablet', 45.00, 'Fluconazole (150mg)', 88991, 0);
        """, (REC_MED_ID,))
        cursor.execute("INSERT INTO medicine_uses (medicine_id, use_name) VALUES (?, 'Fungal infection');", (REC_MED_ID,))
        cursor.execute("INSERT INTO substitutes (medicine_id, substitute_name, substitute_medicine_id) VALUES (?, 'Forcan 150 Test Tablet', NULL);", (REC_MED_ID,))
        conn.commit()
    finally:
        conn.close()

def test_recommendation_pipeline_fungal_infection():
    payload = {
        "disease": "Fungal infection",
        "max_recommendations": 3
    }
    response = client.post("/api/v1/recommendations/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["disease"] == "Fungal infection"
    assert data["recommendation_count"] > 0
    
    rec = data["recommendations"][0]
    
    # Exact JSON key requirements check from User Prompt
    assert "medicine" in rec
    assert "reason" in rec
    assert "confidence" in rec
    assert "alternatives" in rec
    
    assert len(rec["medicine"]) > 0
    assert len(rec["reason"]) > 0
    assert "%" in rec["confidence"]

def test_recommendation_pipeline_pneumonia():
    payload = {
        "disease": "Pneumonia"
    }
    response = client.post("/api/v1/recommendations/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation_count"] > 0
    rec = data["recommendations"][0]
    assert rec["confidence_score"] > 0.5
