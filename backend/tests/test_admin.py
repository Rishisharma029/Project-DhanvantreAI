import os
import sys
import uuid
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.database import init_user_db
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def admin_tokens():
    init_user_db()
    pwd = "Password123!"

    # Register standard user
    std_email = f"std_user_{uuid.uuid4().hex[:8]}@example.com"
    r_std = client.post("/api/v1/auth/register", json={"email": std_email, "password": pwd, "full_name": "Standard User", "role": "user"})
    assert r_std.status_code == 201, f"Failed std user reg: {r_std.text}"
    
    std_res = client.post("/api/v1/auth/login", json={"email": std_email, "password": pwd})
    assert std_res.status_code == 200, f"Failed std login: {std_res.text}"
    std_token = std_res.json()["access_token"]

    # Register admin user
    admin_email = f"admin_user_{uuid.uuid4().hex[:8]}@example.com"
    r_adm = client.post("/api/v1/auth/register", json={"email": admin_email, "password": pwd, "full_name": "Admin User", "role": "user"})
    assert r_adm.status_code == 201, f"Failed admin user reg: {r_adm.text}"

    # Directly update DB role to admin to ensure admin privilege
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("UPDATE users SET role = 'admin' WHERE email = ?;", (admin_email,))
    conn.commit()
    conn.close()

    admin_res = client.post("/api/v1/auth/login", json={"email": admin_email, "password": pwd})
    assert admin_res.status_code == 200, f"Failed admin login: {admin_res.text}"
    admin_token = admin_res.json()["access_token"]

    return {
        "std_headers": {"Authorization": f"Bearer {std_token}"},
        "admin_headers": {"Authorization": f"Bearer {admin_token}"},
        "std_email": std_email
    }


def test_admin_rbac_forbidden(admin_tokens):
    res = client.get("/api/v1/admin/medicines", headers=admin_tokens["std_headers"])
    assert res.status_code == 403

def test_admin_medicines_crud(admin_tokens):
    payload = {
        "canonical_name": "Admin Test Medicine 500mg",
        "brand_name": "AdminBrand",
        "generic_name": "TestGeneric",
        "composition": "TestGeneric (500mg)",
        "price_inr": 45.0
    }
    create_res = client.post("/api/v1/admin/medicines", json=payload, headers=admin_tokens["admin_headers"])
    assert create_res.status_code == 200
    med_id = create_res.json()["medicine_id"]

    get_res = client.get("/api/v1/admin/medicines", headers=admin_tokens["admin_headers"])
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1

    del_res = client.delete(f"/api/v1/admin/medicines/{med_id}", headers=admin_tokens["admin_headers"])
    assert del_res.status_code == 200

def test_admin_diseases_crud(admin_tokens):
    payload = {
        "name": "Admin Test Disease",
        "severity_level": "Moderate",
        "description": "Disease for admin backend testing",
        "symptoms": ["fever", "chills"]
    }
    create_res = client.post("/api/v1/admin/diseases", json=payload, headers=admin_tokens["admin_headers"])
    assert create_res.status_code == 200
    dis_id = create_res.json()["disease_id"]

    get_res = client.get("/api/v1/admin/diseases", headers=admin_tokens["admin_headers"])
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1

    del_res = client.delete(f"/api/v1/admin/diseases/{dis_id}", headers=admin_tokens["admin_headers"])
    assert del_res.status_code == 200

def test_admin_users_governance(admin_tokens):
    get_res = client.get("/api/v1/admin/users", headers=admin_tokens["admin_headers"])
    assert get_res.status_code == 200
    users = get_res.json()
    assert len(users) >= 2

    # Pick non-admin target user so admin does not demote itself
    target_user = next((u for u in users if u["email"] == admin_tokens["std_email"]), users[0])
    target_id = target_user["id"]

    put_res = client.put(f"/api/v1/admin/users/{target_id}/role", json={"role": "doctor", "is_active": True}, headers=admin_tokens["admin_headers"])
    assert put_res.status_code == 200
    assert put_res.json()["role"] == "doctor"

def test_admin_reports_and_db_stats(admin_tokens):
    rep_res = client.get("/api/v1/admin/reports/stats", headers=admin_tokens["admin_headers"])
    assert rep_res.status_code == 200
    assert rep_res.json()["total_users"] >= 2

    db_res = client.get("/api/v1/admin/db/stats", headers=admin_tokens["admin_headers"])
    assert db_res.status_code == 200
    assert db_res.json()["total_tables"] >= 10

    vac_res = client.post("/api/v1/admin/db/vacuum", headers=admin_tokens["admin_headers"])
    assert vac_res.status_code == 200
    assert vac_res.json()["status"] == "Optimized"
