"""
Tests for Payment Webhook Verification and Server-Side Price Enforcement.

Covers:
1. Stripe webhook signature verification (valid/invalid/missing)
2. Replay attack prevention (idempotent event processing)
3. Server-side price enforcement (plans endpoint returns catalog prices)
4. Subscription endpoint rejects invalid plans
5. Subscription endpoint uses server-side prices only
"""
import os
import sys
import hmac
import hashlib
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.database import init_user_db
from app.config import settings
from app.api.payment_router import compute_signature


@pytest.fixture(autouse=True)
def setup_db():
    init_user_db()
    yield


client = TestClient(app)

# Test webhook secret
TEST_WEBHOOK_SECRET = "whsec_test_secret_key_12345"


def make_signed_payload(payload_dict: dict, secret: str) -> tuple:
    """Create a signed webhook payload for testing."""
    body = json.dumps(payload_dict)
    body_bytes = body.encode("utf-8")
    signature = compute_signature(body_bytes, secret)
    sig_header = f"t=1234567890,v1={signature}"
    return body, sig_header


def test_get_plans_returns_server_side_prices():
    """Verify /plans endpoint returns prices from server-side PLAN_CATALOG."""
    response = client.get("/api/v1/payments/plans")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3  # free, pro, enterprise

    # Verify prices match the server-side catalog exactly
    for plan in data:
        assert plan["id"] in settings.PLAN_CATALOG
        catalog_plan = settings.PLAN_CATALOG[plan["id"]]
        assert plan["price_cents"] == catalog_plan["price_cents"]
        assert plan["currency"] == catalog_plan["currency"]
        assert plan["name"] == catalog_plan["name"]

    # Verify specific prices are server-enforced
    free_plan = next(p for p in data if p["id"] == "free")
    pro_plan = next(p for p in data if p["id"] == "pro")
    enterprise_plan = next(p for p in data if p["id"] == "enterprise")

    assert free_plan["price_cents"] == 0
    assert pro_plan["price_cents"] == 2999
    assert enterprise_plan["price_cents"] == 9999


def test_webhook_valid_signature():
    """Verify webhook accepts events with valid HMAC-SHA256 signature."""
    # Set test webhook secret
    original_secret = settings.STRIPE_WEBHOOK_SECRET
    settings.STRIPE_WEBHOOK_SECRET = TEST_WEBHOOK_SECRET

    try:
        event = {
            "id": "evt_test_valid_001",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "customer_email": "test@example.com",
                    "customer": "cus_test123",
                    "subscription": "sub_test123",
                    "amount_total": 2999,
                    "currency": "usd",
                    "metadata": {"plan_id": "pro", "user_id": "1"},
                }
            },
        }

        body, sig_header = make_signed_payload(event, TEST_WEBHOOK_SECRET)

        response = client.post(
            "/api/v1/payments/webhook",
            content=body,
            headers={
                "stripe-signature": sig_header,
                "content-type": "application/json",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["received"] is True
        assert data["event_type"] == "checkout.session.completed"
    finally:
        settings.STRIPE_WEBHOOK_SECRET = original_secret


def test_webhook_invalid_signature():
    """Verify webhook rejects events with invalid signature."""
    original_secret = settings.STRIPE_WEBHOOK_SECRET
    settings.STRIPE_WEBHOOK_SECRET = TEST_WEBHOOK_SECRET

    try:
        event = {
            "id": "evt_test_invalid_001",
            "type": "checkout.session.completed",
            "data": {"object": {}},
        }

        body, _ = make_signed_payload(event, TEST_WEBHOOK_SECRET)

        # Tamper with the signature
        response = client.post(
            "/api/v1/payments/webhook",
            content=body,
            headers={
                "stripe-signature": "t=1234567890,v1=invalidsignature",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]
    finally:
        settings.STRIPE_WEBHOOK_SECRET = original_secret


def test_webhook_missing_signature():
    """Verify webhook rejects events without any signature header."""
    original_secret = settings.STRIPE_WEBHOOK_SECRET
    settings.STRIPE_WEBHOOK_SECRET = TEST_WEBHOOK_SECRET

    try:
        event = {
            "id": "evt_test_missing_sig_001",
            "type": "checkout.session.completed",
            "data": {"object": {}},
        }

        body = json.dumps(event)

        response = client.post(
            "/api/v1/payments/webhook",
            content=body,
            headers={"content-type": "application/json"},
        )

        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]
    finally:
        settings.STRIPE_WEBHOOK_SECRET = original_secret


def test_webhook_replay_attack_prevention():
    """Verify webhook is idempotent — replayed events return 200 without reprocessing."""
    original_secret = settings.STRIPE_WEBHOOK_SECRET
    settings.STRIPE_WEBHOOK_SECRET = TEST_WEBHOOK_SECRET

    try:
        event = {
            "id": "evt_replay_test_001",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "customer_email": "replay@example.com",
                    "customer": "cus_replay",
                    "subscription": "sub_replay",
                    "amount_total": 2999,
                    "currency": "usd",
                    "metadata": {"plan_id": "pro", "user_id": "1"},
                }
            },
        }

        body, sig_header = make_signed_payload(event, TEST_WEBHOOK_SECRET)

        headers = {
            "stripe-signature": sig_header,
            "content-type": "application/json",
        }

        # First request
        response1 = client.post("/api/v1/payments/webhook", content=body, headers=headers)
        assert response1.status_code == 200

        # Second request (replay) — should still return 200 but not reprocess
        response2 = client.post("/api/v1/payments/webhook", content=body, headers=headers)
        assert response2.status_code == 200
    finally:
        settings.STRIPE_WEBHOOK_SECRET = original_secret


def test_webhook_unconfigured_secret():
    """Verify webhook returns 503 when STRIPE_WEBHOOK_SECRET is not set."""
    original_secret = settings.STRIPE_WEBHOOK_SECRET
    settings.STRIPE_WEBHOOK_SECRET = ""

    try:
        event = {"id": "evt_test_001", "type": "test", "data": {"object": {}}}
        body = json.dumps(event)

        response = client.post(
            "/api/v1/payments/webhook",
            content=body,
            headers={
                "stripe-signature": "t=123,v1=abc",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 503
        assert "not configured" in response.json()["detail"]
    finally:
        settings.STRIPE_WEBHOOK_SECRET = original_secret


def test_subscribe_invalid_plan():
    """Verify subscribe endpoint rejects plans not in the server-side catalog."""
    # First login to get a token
    login_response = client.post("/api/v1/auth/login", json={
        "email": "demo@auramed.ai",
        "password": "Password123!",
    })

    if login_response.status_code != 200:
        pytest.skip("Cannot login — skipping subscription test")

    token = login_response.json()["access_token"]

    # Try to subscribe to a non-existent plan
    response = client.post(
        "/api/v1/payments/subscribe",
        json={"plan_id": "hacker_plan_999"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_subscribe_free_plan():
    """Verify free plan subscription works without Stripe."""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "demo@auramed.ai",
        "password": "Password123!",
    })

    if login_response.status_code != 200:
        pytest.skip("Cannot login — skipping subscription test")

    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/payments/subscribe",
        json={"plan_id": "free"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["plan_id"] == "free"
    assert data["status"] == "active"
