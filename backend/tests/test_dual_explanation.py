import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.dual_explanation_engine import (
    generate_patient_explanation, generate_professional_explanation, run_dual_explanation_engine
)
from app.schemas.explanation_schema import ExplanationRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_patient_mode_explanation():
    """Test Patient Mode simple lay language generation."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    res = generate_patient_explanation("Paracetamol", ["fever"], conn)
    conn.close()

    assert "Paracetamol" in res.summary
    assert len(res.lifestyle_care_steps) > 0
    assert len(res.red_flag_warnings) > 0

def test_professional_mode_explanation():
    """Test Professional Mode clinical terminology, mechanism of action, and contraindications."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    res = generate_professional_explanation("Paracetamol", ["fever"], conn)
    conn.close()

    assert res.icd11_code != ""
    assert "COX" in res.mechanism_of_action
    assert len(res.evidence_citations) > 0
    assert len(res.contraindications) > 0
    assert res.black_box_warnings is not None

def test_dual_mode_engine():
    """Test running engine for both modes simultaneously."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = ExplanationRequest(disease_or_medicine_name="Amoxicillin", mode="BOTH")
    res = run_dual_explanation_engine(req, conn)
    conn.close()

    assert res.patient_explanation is not None
    assert res.professional_explanation is not None
    assert "cell wall" in res.professional_explanation.mechanism_of_action.lower()

def test_explanation_api_endpoint():
    """Test /api/v1/explanation/generate HTTP API endpoint."""
    payload = {
        "disease_or_medicine_name": "Aspirin",
        "reported_symptoms": ["chest pain"],
        "mode": "BOTH"
    }
    response = client.post(f"{settings.API_V1_STR}/explanation/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "patient_explanation" in data
    assert "professional_explanation" in data
    prof = data["professional_explanation"]
    assert "mechanism_of_action" in prof
    assert "evidence_citations" in prof
    assert "contraindications" in prof
