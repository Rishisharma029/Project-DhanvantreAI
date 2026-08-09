import os
import sys
import sqlite3
import pytest

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.database import init_user_db
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    # Clear user tables between tests
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM revoked_jwt_tokens;")
    cursor.execute("DELETE FROM user_medical_reports;")
    cursor.execute("DELETE FROM user_symptom_history;")
    cursor.execute("DELETE FROM user_medication_history;")
    cursor.execute("DELETE FROM user_medical_profiles;")
    cursor.execute("DELETE FROM chat_messages;")
    cursor.execute("DELETE FROM chat_sessions;")
    cursor.execute("DELETE FROM auth_tokens;")
    cursor.execute("DELETE FROM refresh_tokens;")
    cursor.execute("DELETE FROM users;")
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()



def test_register_and_login_user():
    # 1. Register User
    reg_payload = {
        "email": "testuser@medical.org",
        "password": "Password123!",
        "full_name": "Test User",
        "role": "user"
    }
    response = client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@medical.org"
    assert data["role"] == "user"
    assert data["is_active"] is True

    # 2. Prevent Duplicate Registration
    dup_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_res.status_code == 400
    assert "already registered" in dup_res.json()["detail"]

    # 3. Login User
    login_payload = {
        "email": "testuser@medical.org",
        "password": "Password123!"
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    tokens = login_res.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # 4. Fetch User Profile (/me)
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "testuser@medical.org"

def test_token_refresh_and_logout():
    reg_payload = {
        "email": "refreshtest@medical.org",
        "password": "Password123!",
        "full_name": "Refresh User"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_res = client.post("/api/v1/auth/login", json={"email": "refreshtest@medical.org", "password": "Password123!"})
    tokens = login_res.json()

    # Refresh token
    refresh_res = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh_res.status_code == 200
    new_tokens = refresh_res.json()
    assert new_tokens["access_token"] != tokens["access_token"]

    # Logout and attempt using old refresh token
    headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
    logout_res = client.post("/api/v1/auth/logout", json={"refresh_token": new_tokens["refresh_token"]}, headers=headers)
    assert logout_res.status_code == 200

    failed_refresh = client.post("/api/v1/auth/refresh", json={"refresh_token": new_tokens["refresh_token"]})
    assert failed_refresh.status_code == 401

def test_rbac_permissions():
    # Register User
    client.post("/api/v1/auth/register", json={"email": "std_user@med.org", "password": "password123", "full_name": "Std User", "role": "user"})
    u_login = client.post("/api/v1/auth/login", json={"email": "std_user@med.org", "password": "password123"}).json()
    u_headers = {"Authorization": f"Bearer {u_login['access_token']}"}

    # Register Doctor
    client.post("/api/v1/auth/register", json={"email": "doctor@med.org", "password": "password123", "full_name": "Dr. Smith", "role": "doctor"})
    d_login = client.post("/api/v1/auth/login", json={"email": "doctor@med.org", "password": "password123"}).json()
    d_headers = {"Authorization": f"Bearer {d_login['access_token']}"}

    # Register Admin
    client.post("/api/v1/auth/register", json={"email": "admin@med.org", "password": "password123", "full_name": "Admin User", "role": "admin"})
    a_login = client.post("/api/v1/auth/login", json={"email": "admin@med.org", "password": "password123"}).json()
    a_headers = {"Authorization": f"Bearer {a_login['access_token']}"}

    # Test /doctor-only
    assert client.get("/api/v1/auth/doctor-only", headers=u_headers).status_code == 403
    assert client.get("/api/v1/auth/doctor-only", headers=d_headers).status_code == 200
    assert client.get("/api/v1/auth/doctor-only", headers=a_headers).status_code == 200

    # Test /admin-only
    assert client.get("/api/v1/auth/admin-only", headers=u_headers).status_code == 403
    assert client.get("/api/v1/auth/admin-only", headers=d_headers).status_code == 403
    assert client.get("/api/v1/auth/admin-only", headers=a_headers).status_code == 200

def test_password_reset_flow():
    client.post("/api/v1/auth/register", json={"email": "resetuser@med.org", "password": "oldPassword123", "full_name": "Reset User"})
    
    # Request reset token
    forgot_res = client.post("/api/v1/auth/forgot-password", json={"email": "resetuser@med.org"})
    assert forgot_res.status_code == 200
    reset_token = forgot_res.json()["reset_token"]

    # Reset password
    reset_res = client.post("/api/v1/auth/reset-password", json={"token": reset_token, "new_password": "newPassword123"})
    assert reset_res.status_code == 200

    # Login with new password
    new_login = client.post("/api/v1/auth/login", json={"email": "resetuser@med.org", "password": "newPassword123"})
    assert new_login.status_code == 200

def test_google_oauth():
    oauth_res = client.post("/api/v1/auth/google", json={"id_token": "sample-google-id-token-123"})
    assert oauth_res.status_code == 200
    assert "access_token" in oauth_res.json()
