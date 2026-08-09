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
    email = f"notif_user_{uuid.uuid4().hex[:8]}@example.com"
    password = "SecurePassword123!"

    # Register
    reg_payload = {
        "email": email,
        "password": password,
        "full_name": "Notification Test User"
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
    return {"Authorization": f"Bearer {token}", "email": email}

def test_send_password_reset_notification(auth_headers):
    payload = {
        "email": auth_headers["email"],
        "reset_token": "sample-reset-token-998877"
    }
    response = client.post("/api/v1/notifications/send-password-reset", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["notification_type"] == "Password Reset"
    assert data["status"] == "SENT"
    assert "sample-reset-token-998877" in data["message"]

def test_send_report_ready_notification(auth_headers):
    payload = {
        "report_title": "Lipid Profile Test",
        "report_type": "Blood Test",
        "recipient_email": auth_headers["email"]
    }
    response = client.post("/api/v1/notifications/send-report-ready", json=payload, headers={"Authorization": auth_headers["Authorization"]})
    assert response.status_code == 200
    data = response.json()

    assert data["notification_type"] == "Report Ready"
    assert "Lipid Profile Test" in data["title"]
    assert data["status"] == "SENT"

def test_send_followup_reminder_notification(auth_headers):
    payload = {
        "doctor_name": "Dr. V. Kapoor",
        "visit_date": "2026-08-10",
        "reason": "Cardiology Check-up",
        "recipient_email": auth_headers["email"]
    }
    response = client.post("/api/v1/notifications/send-followup-reminder", json=payload, headers={"Authorization": auth_headers["Authorization"]})
    assert response.status_code == 200
    data = response.json()

    assert data["notification_type"] == "Follow-up Reminder"
    assert "Dr. V. Kapoor" in data["message"]
    assert data["status"] == "SENT"

def test_get_my_notifications_inbox(auth_headers):
    response = client.get("/api/v1/notifications/my-notifications", headers={"Authorization": auth_headers["Authorization"]})
    assert response.status_code == 200
    inbox = response.json()

    assert len(inbox) >= 2
    assert any(n["notification_type"] == "Report Ready" for n in inbox)
    assert any(n["notification_type"] == "Follow-up Reminder" for n in inbox)
