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

GUARD_MED_ID = 996611

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (GUARD_MED_ID,))
        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (996611, 'Cipla Ltd');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (?, 'Paracetamol 650mg Guard Tablet', 'Paracetamol 650mg Guard Tablet', 'Paracetamol', 'paracetamol 650mg guard tablet', 25.00, 'Paracetamol (650mg)', 996611);
        """, (GUARD_MED_ID,))
        conn.commit()
    finally:
        conn.close()

def test_valid_clinical_guardrail_passed():
    payload = {
        "medicine_name": "Paracetamol",
        "dosage_text": "500mg every 6 hours",
        "patient_age": 30,
        "has_disclaimer": True
    }
    response = client.post("/api/v1/guardrails/verify", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_valid"] is True
    assert data["status"] == "PASSED"
    assert data["total_violations"] == 0

def test_hallucinated_drug_name_regeneration_trigger():
    payload = {
        "medicine_name": "FakeHallucinatedDrug123",
        "dosage_text": "500mg daily",
        "patient_age": 30,
        "has_disclaimer": True
    }
    response = client.post("/api/v1/guardrails/verify", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_valid"] is False
    assert data["status"] == "REGENERATE_REQUIRED"
    assert data["total_violations"] >= 1
    assert "HALLUCINATION ALERT" in data["violations"][0]["message"]
    assert "REGENERATION PROMPT" in data["corrective_feedback_prompt"]

def test_dosage_overdose_hazard_trigger():
    payload = {
        "medicine_name": "Paracetamol",
        "dosage_text": "6000mg per 24 hours",
        "patient_age": 30,
        "has_disclaimer": True
    }
    response = client.post("/api/v1/guardrails/verify", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_valid"] is False
    assert data["status"] == "REGENERATE_REQUIRED"
    assert any("OVERDOSE HAZARD" in v["message"] for v in data["violations"])

def test_allergy_contraindication_trigger():
    payload = {
        "medicine_name": "Penicillin V",
        "dosage_text": "250mg daily",
        "patient_age": 30,
        "patient_allergies": ["Penicillin"],
        "has_disclaimer": True
    }
    response = client.post("/api/v1/guardrails/verify", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_valid"] is False
    assert data["status"] == "REGENERATE_REQUIRED"
    assert any("ALLERGY CONTRAINDICATION" in v["message"] for v in data["violations"])

def test_missing_disclaimer_trigger():
    payload = {
        "medicine_name": "Paracetamol",
        "dosage_text": "500mg every 6 hours",
        "patient_age": 30,
        "has_disclaimer": False
    }
    response = client.post("/api/v1/guardrails/verify", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_valid"] is False
    assert data["status"] == "REGENERATE_REQUIRED"
    assert any("SAFETY INSTRUCTION MISSING" in v["message"] for v in data["violations"])
