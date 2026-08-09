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
    cursor.execute("INSERT OR IGNORE INTO symptoms (id, name, severity_weight) VALUES (9990, 'fever', 2), (9991, 'headache', 1), (9992, 'vomiting', 2);")
    cursor.execute("INSERT OR IGNORE INTO diseases (id, name, severity_level, description) VALUES (9990, 'Dengue', 'Severe', 'Mosquito-borne viral infection');")
    cursor.execute("INSERT OR IGNORE INTO disease_symptoms (disease_id, symptom_id) VALUES (9990, 9990), (9990, 9991);")
    conn.commit()
    conn.close()

def test_symptom_extraction_and_canonicalization():
    req_payload = {
        "text": "I have high fever and headache since yesterday"
    }
    response = client.post("/api/v1/symptoms/process", json=req_payload)
    assert response.status_code == 200
    data = response.json()

    assert data["input_text"] == "I have high fever and headache since yesterday"
    canon = [s.lower() for s in data["canonical_symptom_names"]]
    assert "fever" in canon
    assert "headache" in canon
    assert data["overall_severity"] == "Severe"

def test_synonym_resolution_and_deduplication():
    req_payload = {
        "text": "Experiencing severe head pain, puking, and throwing up"
    }
    response = client.post("/api/v1/symptoms/process", json=req_payload)
    assert response.status_code == 200
    data = response.json()

    canon = [s.lower() for s in data["canonical_symptom_names"]]
    assert "headache" in canon
    assert "vomiting" in canon
    assert canon.count("vomiting") == 1

def test_disease_candidate_matching():
    req_payload = {
        "text": "Patient presents with high fever and headache"
    }
    response = client.post("/api/v1/symptoms/process", json=req_payload)
    assert response.status_code == 200
    data = response.json()

    candidates = data["candidate_diseases"]
    assert len(candidates) > 0
    disease_names = [c["disease_name"] for c in candidates]
    assert any(d in disease_names for d in ["Dengue", "Malaria", "Influenza", "Typhoid"])

def test_symptom_search_autocompletion():
    res = client.get("/api/v1/symptoms/search?q=fev")
    assert res.status_code == 200
    results = res.json()
    assert len(results) > 0
    assert "fever" in results[0]["name"].lower()
