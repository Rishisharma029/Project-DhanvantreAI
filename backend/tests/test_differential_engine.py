import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.differential_diagnosis_engine import (
    generate_differential_diagnosis, map_severity_level
)
from app.schemas.differential_schema import DifferentialDiagnosisRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_severity_mapping():
    """Test clinical severity level classification."""
    assert map_severity_level("Acute Coronary Syndrome", 0.90) == "RED_EMERGENCY"
    assert map_severity_level("Pneumonia", 0.85) == "HIGH_URGENT"
    assert map_severity_level("Viral Fever", 0.75) == "MODERATE"

def test_differential_diagnosis_multi_candidates():
    """Test multi-candidate differential diagnosis generation."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = DifferentialDiagnosisRequest(symptoms=["fever", "cough", "headache", "body pain"])
    res = generate_differential_diagnosis(req, conn)
    conn.close()

    assert res.total_candidates_evaluated > 0
    assert len(res.differential_candidates) > 0

    first = res.differential_candidates[0]
    assert first.rank == 1
    assert first.probability_percentage.endswith("%")
    assert isinstance(first.evidence, list)
    assert isinstance(first.missing_findings, list)
    assert first.severity_level in ("RED_EMERGENCY", "HIGH_URGENT", "MODERATE", "LOW_MILD")

def test_differential_api_endpoint():
    """Test /api/v1/differential/diagnose HTTP API endpoint."""
    payload = {
        "symptoms": ["chest pain", "shortness of breath", "sweating"],
        "onset_days": 1
    }
    response = client.post(f"{settings.API_V1_STR}/differential/diagnose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "differential_candidates" in data
    assert len(data["differential_candidates"]) > 0
    candidate = data["differential_candidates"][0]
    assert "probability_percentage" in candidate
    assert "evidence" in candidate
    assert "missing_findings" in candidate
    assert "severity_level" in candidate
