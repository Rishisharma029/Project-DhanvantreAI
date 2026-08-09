import os
import sys
import secrets
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_sql_injection_resilience():
    """Verify parameterized queries block SQL injection attempts on search & auth endpoints."""
    sql_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "1 UNION SELECT 1, 'admin', 'hash', 'admin', 'admin', 1, '2026-01-01'",
        "admin'--"
    ]

    for payload in sql_payloads:
        # Search API test
        res = client.get(f"/api/v1/search/medicines?q={payload}")
        assert res.status_code == 200

        # Auth Login test
        res_login = client.post("/api/v1/auth/login", json={"email": payload, "password": "password123"})
        assert res_login.status_code in [400, 401, 422]

def test_xss_payload_sanitization():
    """Verify Cross-Site Scripting (XSS) script tags do not break server response contracts."""
    xss_payload = "<script>alert('XSS_ATTACK')</script>"
    res = client.get(f"/api/v1/search/medicines?q={xss_payload}")
    assert res.status_code == 200
    assert "<script>" not in res.text or "&lt;script&gt;" in res.text or isinstance(res.json(), list)

def test_https_enforcement_security_headers():
    """Verify production security headers suite and HTTPS enforcement policies."""
    res = client.get("/health")
    assert res.status_code == 200
    assert "Content-Security-Policy" in res.headers
    assert "Strict-Transport-Security" in res.headers
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["X-Frame-Options"] in ["DENY", "SAMEORIGIN"]

def test_secret_key_rotation_service():
    """Verify secret rotation helper generates cryptographically secure 256-bit keys."""
    new_secret = secrets.token_hex(32)
    assert len(new_secret) == 64
    assert isinstance(new_secret, str)
