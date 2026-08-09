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

DOSAGE_TEST_ID = 999955

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (DOSAGE_TEST_ID,))
        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (999955, 'Cipla Ltd');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (?, 'Paracetamol 650mg Test Tablet', 'Paracetamol 650mg Test Tablet', 'Paracetamol', 'paracetamol 650mg test tablet', 20.00, 'Paracetamol (650mg)', 999955);
        """, (DOSAGE_TEST_ID,))
        conn.commit()
    finally:
        conn.close()

def test_paracetamol_dosage_reference():
    response = client.get("/api/v1/dosage/reference?medicine_name=Paracetamol")
    assert response.status_code == 200
    data = response.json()

    assert "Paracetamol" in data["medicine_name"]
    assert "mg" in data["standard_adult_dose"]
    assert "pediatric" in data["pediatric_dose"].lower() or "mg/kg" in data["pediatric_dose"].lower()
    assert "4000 mg" in data["maximum_daily_dose"] or "4" in data["maximum_daily_dose"]
    assert data["route"] == "Oral"
    assert "Every" in data["frequency"] or "hours" in data["frequency"]
    assert "days" in data["duration"]
    assert "Reference information only" in data["disclaimer"]

def test_amoxycillin_dosage_reference():
    response = client.get("/api/v1/dosage/reference?medicine_name=Amoxycillin")
    assert response.status_code == 200
    data = response.json()

    assert "mg" in data["standard_adult_dose"]
    assert "5 - 10 days" in data["duration"] or "days" in data["duration"]
    assert data["route"] == "Oral"
    assert "Reference information only" in data["disclaimer"]

def test_dosage_reference_by_id():
    response = client.get(f"/api/v1/dosage/reference/{DOSAGE_TEST_ID}")
    assert response.status_code == 200
    data = response.json()

    assert "Paracetamol" in data["medicine_name"]
    assert data["route"] == "Oral"
    assert "Reference information only" in data["disclaimer"]
