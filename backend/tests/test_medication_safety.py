import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.medication_safety_ai import evaluate_medication_safety
from app.schemas.med_safety_schema import MedicationSafetyRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_safe_medication_profile():
    """Test completely safe medication profile resulting in 100 Safety Score."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = MedicationSafetyRequest(
        medications=["Paracetamol"],
        patient_age=30,
        is_pregnant=False,
        is_lactating=False,
        egfr_ml_min=90.0,
        alt_ast_u_l=25.0,
        known_allergies=[]
    )
    res = evaluate_medication_safety(req, conn)
    conn.close()

    assert res.safety_score == 100
    assert res.risk_level == "LOW_GREEN"
    assert res.total_alerts_found == 0

def test_high_risk_pregnancy_renal_allergy_profile():
    """Test high risk patient profile triggering pregnancy, renal, and allergy alerts."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = MedicationSafetyRequest(
        medications=["Warfarin", "Amoxicillin", "Ciprofloxacin"],
        patient_age=70,
        is_pregnant=True,
        trimester=3,
        egfr_ml_min=25.0,
        known_allergies=["Penicillin"]
    )
    res = evaluate_medication_safety(req, conn)
    conn.close()

    assert res.safety_score < 50
    assert res.risk_level in ("CRITICAL_RED", "HIGH_ORANGE")
    assert res.total_alerts_found >= 3

    check_names = [c.check_name for c in res.safety_checks if not c.passed]
    assert "PREGNANCY" in check_names
    assert "ALLERGY" in check_names
    assert "RENAL" in check_names

def test_med_safety_api_endpoint():
    """Test /api/v1/med-safety/evaluate HTTP API endpoint."""
    payload = {
        "medications": ["Aspirin", "Ciprofloxacin"],
        "patient_age": 12,
        "is_pregnant": False,
        "known_allergies": []
    }
    response = client.post(f"{settings.API_V1_STR}/med-safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "safety_score" in data
    assert "risk_level" in data
    assert "safety_checks" in data
    assert len(data["safety_checks"]) == 10
