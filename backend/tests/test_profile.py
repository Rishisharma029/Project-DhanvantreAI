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
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_medical_profiles;")
    cursor.execute("DELETE FROM auth_tokens;")
    cursor.execute("DELETE FROM refresh_tokens;")
    cursor.execute("DELETE FROM users;")
    conn.commit()
    conn.close()

def get_auth_headers(email: str, role: str = "user") -> dict:
    """Helper function to register, login, and return Auth header."""
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": f"Name {email}",
        "role": role
    })
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_profile_creation_update_and_bmi():
    headers = get_auth_headers("patient@medical.org", "user")

    # 1. Fetch initial blank profile
    get_res = client.get("/api/v1/profile/me", headers=headers)
    assert get_res.status_code == 200
    p_data = get_res.json()
    assert p_data["allergies"] == []
    assert p_data["bmi"] is None

    # 2. Update Medical Profile
    update_payload = {
        "age": 30,
        "gender": "Male",
        "height_cm": 175.0,
        "weight_kg": 70.0,
        "blood_group": "O+",
        "pregnancy_status": False,
        "allergies": ["Penicillin", "Peanuts"],
        "chronic_diseases": ["Hypertension"],
        "current_medications": ["Lisinopril 10mg"],
        "past_medical_history": "Appendectomy in 2018",
        "family_history": "Father had Diabetes Type 2",
        "smoking_status": "Non-Smoker",
        "alcohol_consumption": "Occasional"
    }

    put_res = client.put("/api/v1/profile/me", json=update_payload, headers=headers)
    assert put_res.status_code == 200
    updated = put_res.json()

    assert updated["age"] == 30
    assert updated["gender"] == "Male"
    assert updated["height_cm"] == 175.0
    assert updated["weight_kg"] == 70.0
    assert updated["bmi"] == 22.86 # 70 / (1.75 * 1.75) = 22.857 -> 22.86
    assert "Penicillin" in updated["allergies"]
    assert "Hypertension" in updated["chronic_diseases"]
    assert "Lisinopril 10mg" in updated["current_medications"]
    assert updated["smoking_status"] == "Non-Smoker"

def test_doctor_patient_chart_lookup():
    user_headers = get_auth_headers("patient2@medical.org", "user")
    doctor_headers = get_auth_headers("dr_smith@hospital.org", "doctor")

    # Fill patient profile
    client.put("/api/v1/profile/me", json={
        "age": 45,
        "blood_group": "B+",
        "chronic_diseases": ["Diabetes Type 2"]
    }, headers=user_headers)

    # Get patient user ID
    user_me = client.get("/api/v1/auth/me", headers=user_headers).json()
    patient_user_id = user_me["id"]

    # 1. Standard user cannot view another user's chart
    denied = client.get(f"/api/v1/profile/user/{patient_user_id}", headers=user_headers)
    assert denied.status_code == 403

    # 2. Doctor can view patient chart
    chart_res = client.get(f"/api/v1/profile/user/{patient_user_id}", headers=doctor_headers)
    assert chart_res.status_code == 200
    assert chart_res.json()["blood_group"] == "B+"
    assert "Diabetes Type 2" in chart_res.json()["chronic_diseases"]

def test_reset_medical_profile():
    headers = get_auth_headers("resetprofile@medical.org", "user")
    client.put("/api/v1/profile/me", json={"age": 25, "blood_group": "AB+"}, headers=headers)

    del_res = client.delete("/api/v1/profile/me", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Medical profile successfully reset"

    # Fetching profile again creates fresh empty record
    fresh_res = client.get("/api/v1/profile/me", headers=headers)
    assert fresh_res.status_code == 200
    assert fresh_res.json()["age"] is None
