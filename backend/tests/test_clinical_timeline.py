import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db
from app.services.clinical_timeline_engine import generate_clinical_timeline
from app.schemas.clinical_timeline_schema import ClinicalTimelineRequest, TimelineStage

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_timeline_generation_5_stages():
    """Verify that all 5 clinical stages are produced in exact sequential order."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = ClinicalTimelineRequest(
        reported_symptoms=["fever", "cough", "body pain"],
        diagnosis_name="Acute Bronchitis",
        prescribed_medicines=["Amoxicillin", "Paracetamol"],
        onset_days_ago=3
    )
    res = generate_clinical_timeline(req, conn)
    conn.close()

    assert res.condition_name == "Acute Bronchitis"
    assert len(res.timeline_nodes) == 5

    stages = [node.stage for node in res.timeline_nodes]
    expected_order = [
        TimelineStage.SYMPTOMS,
        TimelineStage.ASSESSMENT,
        TimelineStage.MEDICINES,
        TimelineStage.FOLLOWUP,
        TimelineStage.RECOVERY
    ]
    assert stages == expected_order
    assert len(res.key_milestones) == 5
    assert len(res.red_flag_warnings) >= 3

def test_timeline_api_endpoint():
    """Test HTTP POST /api/v1/timeline/generate REST endpoint."""
    payload = {
        "reported_symptoms": ["headache", "fatigue"],
        "diagnosis_name": "Viral Fever",
        "prescribed_medicines": ["Paracetamol"],
        "onset_days_ago": 1
    }
    response = client.post(f"{settings.API_V1_STR}/timeline/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "timeline_nodes" in data
    assert len(data["timeline_nodes"]) == 5
    assert data["timeline_nodes"][0]["stage"] == "SYMPTOMS"
    assert data["timeline_nodes"][1]["stage"] == "ASSESSMENT"
    assert data["timeline_nodes"][2]["stage"] == "MEDICINES"
    assert data["timeline_nodes"][3]["stage"] == "FOLLOWUP"
    assert data["timeline_nodes"][4]["stage"] == "RECOVERY"
