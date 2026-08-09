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
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (99911, 'Glaxo SmithKline');")
        cursor.execute("""
            INSERT OR IGNORE INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (99911, 'Augmentin 625 Duo Tablet', 'Augmentin 625 Duo Tablet', 'Amoxycillin + Clavulanic Acid', 'augmentin 625 duo tablet', 223.42, 'Amoxycillin (500mg) + Clavulanic Acid (125mg)', 99911);
        """)
        cursor.execute("INSERT OR IGNORE INTO medicine_ingredients (medicine_id, ingredient_name, strength, unit) VALUES (99911, 'Amoxycillin', 500.0, 'mg'), (99911, 'Clavulanic Acid', 125.0, 'mg');")
        conn.commit()
    finally:
        conn.close()

def test_allergy_contraindication_anaphylaxis():
    payload = {
        "medicine_name": "Augmentin 625 Duo Tablet",
        "patient_profile": {
            "age": 35,
            "allergies": ["Amoxycillin"]
        }
    }
    response = client.post("/api/v1/safety/validate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_score"] == 0.0
    assert data["safety_grade"] == "CONTRAINDICATED"
    assert data["is_safe_to_take"] is False
    assert any("ALLERGY" in w["message"] for w in data["warnings"])

def test_pregnancy_category_d_x_contraindication():
    payload = {
        "medicine_name": "Methotrexate 5mg Tablet",
        "patient_profile": {
            "age": 28,
            "pregnancy_status": True
        }
    }
    response = client.post("/api/v1/safety/validate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_score"] < 60.0
    assert data["is_safe_to_take"] is False
    assert any("PREGNANCY" in w["message"] for w in data["warnings"])

def test_pediatric_aspirin_warning():
    payload = {
        "medicine_name": "Aspirin 75mg Tablet",
        "patient_profile": {
            "age": 10
        }
    }
    response = client.post("/api/v1/safety/validate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_score"] < 85.0
    assert any("PEDIATRIC" in w["message"] for w in data["warnings"])

def test_renal_impairment_ibuprofen_warning():
    payload = {
        "medicine_name": "Ibuprofen 400mg Tablet",
        "patient_profile": {
            "age": 55,
            "chronic_diseases": ["Chronic Kidney Disease"]
        }
    }
    response = client.post("/api/v1/safety/validate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_score"] < 60.0
    assert any("RENAL" in w["message"] for w in data["warnings"])

def test_clean_safe_patient_profile():
    payload = {
        "medicine_name": "Paracetamol 500mg Tablet",
        "patient_profile": {
            "age": 30,
            "allergies": [],
            "chronic_diseases": [],
            "current_medications": []
        }
    }
    response = client.post("/api/v1/safety/validate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_score"] == 100.0
    assert data["safety_grade"] == "SAFE"
    assert data["is_safe_to_take"] is True
    assert data["total_warnings"] == 0
