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

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO symptoms (id, name, severity_weight) VALUES (8881, 'fever', 2), (8882, 'headache', 1), (8883, 'chills', 2), (8884, 'joint pain', 2);")
    cursor.execute("INSERT OR IGNORE INTO diseases (id, name, severity_level, description) VALUES (8881, 'Dengue', 'Severe', 'Viral illness transmitted by mosquitoes');")
    cursor.execute("INSERT OR IGNORE INTO disease_symptoms (disease_id, symptom_id) VALUES (8881, 8881), (8881, 8882), (8881, 8883), (8881, 8884);")
    cursor.execute("INSERT OR IGNORE INTO disease_precautions (disease_id, precaution) VALUES (8881, 'Use mosquito repellent'), (8881, 'Stay hydrated');")
    conn.commit()
    conn.close()

def test_disease_prediction_with_matching_and_missing_symptoms():
    payload = {
        "symptoms": ["fever", "headache"],
        "top_n": 5
    }
    response = client.post("/api/v1/disease-prediction/predict", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["total_matches_found"] > 0
    disease_names = [d["disease_name"] for d in data["top_diseases"]]
    assert len(disease_names) > 0
    
    top = data["top_diseases"][0]
    assert top["confidence"] > 0.0
    assert top["confidence_percentage"] > 0.0
    assert top["severity"] in ["Emergency", "Severe", "Moderate", "Mild"]
    
    # Matching Symptoms assertion
    assert len(top["matching_symptoms"]) > 0

    # Missing Symptoms assertion
    assert isinstance(top["missing_symptoms"], list)

def test_disease_prediction_empty_symptoms():
    response = client.post("/api/v1/disease-prediction/predict", json={"symptoms": ["nonexistentsymptomxyz"]})
    assert response.status_code == 200
    data = response.json()
    assert data["total_matches_found"] == 0
    assert data["top_diseases"] == []
