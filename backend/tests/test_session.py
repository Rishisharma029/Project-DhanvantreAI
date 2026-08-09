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
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM revoked_jwt_tokens;")
    cursor.execute("DELETE FROM user_medical_reports;")
    cursor.execute("DELETE FROM user_symptom_history;")
    cursor.execute("DELETE FROM user_medication_history;")
    cursor.execute("DELETE FROM chat_messages;")
    cursor.execute("DELETE FROM chat_sessions;")
    cursor.execute("DELETE FROM user_medical_profiles;")
    cursor.execute("DELETE FROM auth_tokens;")
    cursor.execute("DELETE FROM refresh_tokens;")
    cursor.execute("DELETE FROM users;")
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()



def get_auth_headers(email: str) -> dict:
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": f"User {email}",
        "role": "user"
    })
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_session_lifecycle_and_context_memory():
    headers = get_auth_headers("chatuser@medical.org")

    # 1. Create Session
    create_res = client.post("/api/v1/sessions", json={"title": "Fever & Headaches"}, headers=headers)
    assert create_res.status_code == 201
    s_data = create_res.json()
    session_uuid = s_data["session_uuid"]
    assert s_data["title"] == "Fever & Headaches"

    # 2. Append First Message
    msg1_res = client.post(f"/api/v1/sessions/{session_uuid}/messages", json={
        "content": "What medication should I take for a mild fever?",
        "metadata": {"symptom": "fever", "severity": "mild"}
    }, headers=headers)
    assert msg1_res.status_code == 200

    # 3. Append Second Message
    msg2_res = client.post(f"/api/v1/sessions/{session_uuid}/messages", json={
        "content": "Does Paracetamol interact with Ibuprofen?"
    }, headers=headers)
    assert msg2_res.status_code == 200

    # 4. Resume Session & Check AI Context Memory
    resume_res = client.get(f"/api/v1/sessions/{session_uuid}", headers=headers)
    assert resume_res.status_code == 200
    r_data = resume_res.json()
    assert r_data["message_count"] == 4 # 2 user questions + 2 simulated AI answers
    assert len(r_data["ai_context_memory"]) == 4

    # Verify memory structure format
    memory = r_data["ai_context_memory"]
    assert memory[0]["role"] == "user"
    assert "mild fever" in memory[0]["content"]
    assert memory[1]["role"] == "assistant"

def test_list_and_delete_sessions():
    headers = get_auth_headers("sessionlist@medical.org")

    s1 = client.post("/api/v1/sessions", json={"title": "Consultation 1"}, headers=headers).json()
    s2 = client.post("/api/v1/sessions", json={"title": "Consultation 2"}, headers=headers).json()

    # List Sessions
    list_res = client.get("/api/v1/sessions", headers=headers)
    assert list_res.status_code == 200
    sessions = list_res.json()
    assert len(sessions) == 2

    # Delete Session
    del_res = client.delete(f"/api/v1/sessions/{s1['session_uuid']}", headers=headers)
    assert del_res.status_code == 200

    # Verify session count is 1
    after_del = client.get("/api/v1/sessions", headers=headers).json()
    assert len(after_del) == 1
    assert after_del[0]["session_uuid"] == s2["session_uuid"]

def test_session_cross_user_isolation():
    headers1 = get_auth_headers("user1@med.org")
    headers2 = get_auth_headers("user2@med.org")

    s1 = client.post("/api/v1/sessions", json={"title": "User 1 Private Consultation"}, headers=headers1).json()

    # User 2 attempting to view or resume User 1's session should fail
    unauth_get = client.get(f"/api/v1/sessions/{s1['session_uuid']}", headers=headers2)
    assert unauth_get.status_code == 404
