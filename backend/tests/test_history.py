import os
import sys
import uuid
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.database import init_user_db
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    init_user_db()
    email = f"history_user_{uuid.uuid4().hex[:8]}@example.com"
    password = "SecurePassword123!"

    # Register
    reg_payload = {
        "email": email,
        "password": password,
        "full_name": "History Test User"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201

    # Login
    login_payload = {
        "email": email,
        "password": password
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_medical_reports_crud(auth_headers):
    report_payload = {
        "title": "Complete Blood Count",
        "report_type": "Blood Test",
        "report_date": "2026-07-15",
        "summary_notes": "Hemoglobin normal, WBC slightly elevated."
    }
    post_res = client.post("/api/v1/history/reports", json=report_payload, headers=auth_headers)
    assert post_res.status_code == 200
    report_data = post_res.json()
    assert report_data["title"] == "Complete Blood Count"

    get_res = client.get("/api/v1/history/reports", headers=auth_headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1

def test_symptom_history_crud(auth_headers):
    sym_payload = {
        "symptom_name": "Acute High Fever",
        "severity": "Severe",
        "onset_date": "2026-07-10",
        "resolution_date": "2026-07-14",
        "notes": "Resolved with Paracetamol"
    }
    post_res = client.post("/api/v1/history/symptoms", json=sym_payload, headers=auth_headers)
    assert post_res.status_code == 200
    sym_data = post_res.json()
    assert sym_data["symptom_name"] == "Acute High Fever"

    get_res = client.get("/api/v1/history/symptoms", headers=auth_headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1

def test_medication_history_crud(auth_headers):
    med_payload = {
        "medicine_name": "Amoxicillin 500mg",
        "dosage": "500mg three times daily",
        "start_date": "2026-07-10",
        "end_date": "2026-07-17",
        "side_effects_noted": "Mild nausea"
    }
    post_res = client.post("/api/v1/history/medicines", json=med_payload, headers=auth_headers)
    assert post_res.status_code == 200
    med_data = post_res.json()
    assert med_data["medicine_name"] == "Amoxicillin 500mg"

    get_res = client.get("/api/v1/history/medicines", headers=auth_headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1

def test_followup_visits_crud(auth_headers):
    visit_payload = {
        "doctor_name": "Dr. A. Sharma",
        "reason": "Post-fever clinical review",
        "visit_date": "2026-08-05",
        "is_completed": False,
        "clinical_notes": "Follow up for complete blood count verification"
    }
    post_res = client.post("/api/v1/history/followups", json=visit_payload, headers=auth_headers)
    assert post_res.status_code == 200
    visit_data = post_res.json()
    assert visit_data["doctor_name"] == "Dr. A. Sharma"

    get_res = client.get("/api/v1/history/followups", headers=auth_headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1

def test_unified_medical_history_summary(auth_headers):
    response = client.get("/api/v1/history/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["total_reports"] >= 1
    assert data["total_symptoms"] >= 1
    assert data["total_medicines"] >= 1
    assert data["total_followups"] >= 1
