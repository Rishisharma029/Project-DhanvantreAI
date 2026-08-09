import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.medical_reasoning_engine import (
    collect_evidence, evaluate_differential_diagnoses, evaluate_physician_reasoning
)
from app.schemas.reasoning_schema import PhysicianReasoningRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_evidence_collection():
    """Test evidence collection and severity multiplier calculation."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = PhysicianReasoningRequest(
        reported_symptoms=["chest pain", "shortness of breath"],
        severity_scale="Severe",
        onset_days=2,
        patient_age=50,
        chronic_conditions=["Hypertension"]
    )
    evidence = collect_evidence(req, conn)
    conn.close()

    assert len(evidence["symptoms"]) == 2
    assert evidence["severity_multiplier"] == 1.25
    assert evidence["onset_days"] == 2

def test_differential_rule_in_rule_out():
    """Test differential diagnosis Rule-In / Rule-Out evaluation."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    candidates = evaluate_differential_diagnoses(["fever", "cough", "headache"], conn)
    conn.close()

    assert isinstance(candidates, list)
    if candidates:
        first = candidates[0]
        assert "disease_name" in first
        assert "status" in first
        assert first["status"] in ("RULED_IN", "RULED_OUT")
        assert "match_rationale" in first

def test_full_physician_reasoning_eval():
    """Test complete physician reasoning execution."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = PhysicianReasoningRequest(reported_symptoms=["fever", "chills", "body pain"])
    res = evaluate_physician_reasoning(req, conn)
    conn.close()

    assert res.primary_diagnosis != ""
    assert res.rule_in_rationale != ""
    assert len(res.supporting_evidence) > 0
    assert isinstance(res.differential_matrix, list)

def test_reasoning_api_endpoints():
    """Test /api/v1/reasoning/evaluate and /api/v1/reasoning/differential-matrix endpoints."""
    payload = {
        "reported_symptoms": ["chest pain", "sweating", "nausea"],
        "onset_days": 1,
        "severity_scale": "Severe",
        "patient_age": 55,
        "chronic_conditions": ["Diabetes"]
    }
    response = client.post(f"{settings.API_V1_STR}/reasoning/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "primary_diagnosis" in data
    assert "rule_in_rationale" in data
    assert "differential_matrix" in data

    diff_response = client.post(f"{settings.API_V1_STR}/reasoning/differential-matrix", json=payload)
    assert diff_response.status_code == 200
    diff_data = diff_response.json()
    assert "differential_matrix" in diff_data
