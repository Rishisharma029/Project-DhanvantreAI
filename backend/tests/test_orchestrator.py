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

ORCH_DIS_ID = 997711
ORCH_MED_ID = 997722

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        # Setup Disease & Symptom
        cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?;", (ORCH_DIS_ID,))
        cursor.execute("DELETE FROM diseases WHERE id = ?;", (ORCH_DIS_ID,))
        cursor.execute("""
            INSERT INTO diseases (id, name, severity_level, description)
            VALUES (?, 'Viral Influenza Test', 'Moderate', 'Acute respiratory infection');
        """, (ORCH_DIS_ID,))
        
        cursor.execute("INSERT OR IGNORE INTO symptoms (name) VALUES ('fever');")
        cursor.execute("SELECT id FROM symptoms WHERE name = 'fever' LIMIT 1;")
        sym_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?);", (ORCH_DIS_ID, sym_id))

        conn.commit()
    finally:
        conn.close()

def test_build_prompt_endpoint():
    payload = {
        "query": "I have high fever and body ache",
        "patient_age": 35,
        "patient_gender": "female",
        "allergies": ["Penicillin"],
        "chronic_diseases": ["Asthma"],
        "current_medications": ["Albuterol"]
    }
    response = client.post("/api/v1/orchestrator/build-prompt", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "clinical assistant" in data["system_prompt"].lower()
    assert "Penicillin" in data["user_prompt"]
    assert "Asthma" in data["user_prompt"]
    assert data["injected_context_summary"]["patient_age"] == 35

def test_llm_orchestrator_generate():
    payload = {
        "query": "I have high fever",
        "patient_age": 28,
        "patient_gender": "male",
        "allergies": [],
        "chronic_diseases": [],
        "current_medications": []
    }
    response = client.post("/api/v1/orchestrator/generate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert len(data["extracted_symptoms"]) > 0
    assert "fever" in [s.lower() for s in data["extracted_symptoms"]]
    assert len(data["tool_traces"]) >= 3
    assert data["disclaimer"] is not None

def test_llm_orchestrator_emergency():
    payload = {
        "query": "I have severe crushing chest pain and shortness of breath",
        "patient_age": 60
    }
    response = client.post("/api/v1/orchestrator/generate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_emergency"] is True
    assert data["emergency_alert"] is not None
