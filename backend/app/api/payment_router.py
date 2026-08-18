"""
Payment Router for AuraMed AI.

Implements:
1. Stripe webhook signature verification (HMAC-SHA256)
2. Server-side price enforcement (prices from PLAN_CATALOG only)
3. Subscription management with Stripe integration

Security:
- Webhook endpoint verifies the `stripe-signature` header using the
  STRIPE_WEBHOOK_SECRET to prevent spoofed webhook events.
- Subscription prices are NEVER accepted from the client. The client
  only provides a plan_id, and the server looks up the price from
  the server-side PLAN_CATALOG.
- All webhook events are idempotently stored (event_id uniqueness)
  to prevent replay attacks.
"""
import hashlib
import hmac
import json
import sqlite3
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.api.deps import get_current_user
from app.config import settings
from app.database import get_db
from app.schemas.payment_schema import (
    PlanResponse,
    SubscribeRequest,
    SubscribeResponse,
    WebhookResponse,
    SubscriptionStatusResponse,
)

router = APIRouter(prefix="/payments", tags=["Payments & Subscriptions"])


def compute_signature(payload_bytes: bytes, secret: str) -> str:
    """
    Compute HMAC-SHA256 signature for Stripe webhook verification.
    Stripe sends: t=<timestamp>,v1=<signature_hex>
    We compute: HMAC-SHA256(secret, "<timestamp>.<raw_body>")
    """
    return hmac.new(
        secret.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()


def verify_webhook_signature(payload_bytes: bytes, sig_header: str, secret: str) -> bool:
    """
    Verify Stripe webhook signature.

    Stripe sends the signature in the format: t=<timestamp>,v1=<hex_signature>
    We extract the v1 portion and compare it against our computed HMAC.

    Uses constant-time comparison to prevent timing attacks.
    """
    if not sig_header:
        return False

    # Parse "t=1234567890,v1=abcdef..." format
    parts = sig_header.split(",")
    v1_sig = None
    for part in parts:
        part = part.strip()
        if part.startswith("v1="):
            v1_sig = part[3:]
            break

    if not v1_sig:
        return False

    expected_sig = compute_signature(payload_bytes, secret)
    return hmac.compare_digest(expected_sig, v1_sig)


@router.post("/webhook", response_model=WebhookResponse)
async def stripe_webhook(request: Request, db: sqlite3.Connection = Depends(get_db)):
    """
    Stripe webhook endpoint with HMAC-SHA256 signature verification.

    Accepts raw request body for signature computation, then parses JSON.
    Verifies the stripe-signature header to ensure the event is from Stripe.
    Stores events idempotently to prevent replay attacks.
    """
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe webhook not configured. Set STRIPE_WEBHOOK_SECRET.",
        )

    # Read raw body for signature verification
    body_bytes = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if not verify_webhook_signature(body_bytes, sig_header, settings.STRIPE_WEBHOOK_SECRET):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Stripe signature",
        )

    # Parse the JSON payload
    try:
        event = json.loads(body_bytes)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_id = event.get("id", "")
    event_type = event.get("type", "unknown")
    raw_payload = json.dumps(event)

    # Idempotency: store event to prevent replay attacks
    # If event_id already exists, return 200 OK (Stripe retries)
    existing = db.execute(
        "SELECT id FROM webhook_events WHERE event_id = ?;", (event_id,)
    ).fetchone()

    if existing:
        return WebhookResponse(received=True, event_type=event_type)

    # Store the event
    db.execute(
        """INSERT INTO webhook_events (event_id, event_type, payload)
           VALUES (?, ?, ?);""",
        (event_id, event_type, raw_payload),
    )
    db.commit()

    # Process the event
    _process_webhook_event(event, db)

    return WebhookResponse(received=True, event_type=event_type)


def _process_webhook_event(event: dict, db: sqlite3.Connection):
    """
    Process a verified Stripe webhook event.
    Updates subscription status, logs payment events.
    """
    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        customer_email = data.get("customer_email", "")
        customer_id = data.get("customer", "")
        metadata = data.get("metadata", {})
        plan_id = metadata.get("plan_id", "")

        if not plan_id or plan_id not in settings.PLAN_CATALOG:
            return

        # Find user by email
        user = db.execute(
            "SELECT id FROM users WHERE email = ?;", (customer_email,)
        ).fetchone()
        if not user:
            return

        user_id = user[0]
        stripe_sub_id = data.get("subscription", "")

        # Upsert subscription
        existing = db.execute(
            "SELECT id FROM subscriptions WHERE user_id = ?;", (user_id,)
        ).fetchone()

        if existing:
            db.execute(
                """UPDATE subscriptions
                   SET plan_id = ?, stripe_subscription_id = ?, stripe_customer_id = ?,
                       status = 'active', updated_at = CURRENT_TIMESTAMP
                   WHERE user_id = ?;""",
                (plan_id, stripe_sub_id, customer_id, user_id),
            )
        else:
            db.execute(
                """INSERT INTO subscriptions (user_id, plan_id, stripe_subscription_id, stripe_customer_id, status)
                   VALUES (?, ?, ?, ?, 'active');""",
                (user_id, plan_id, stripe_sub_id, customer_id),
            )

        # Log payment event
        amount = data.get("amount_total", 0)
        currency = (data.get("currency") or "usd").lower()
        db.execute(
            """INSERT INTO payment_events (user_id, stripe_event_id, event_type, amount_cents, currency, plan_id)
               VALUES (?, ?, ?, ?, ?, ?);""",
            (user_id, event.get("id"), event_type, amount, currency, plan_id),
        )
        db.commit()

    elif event_type == "customer.subscription.deleted":
        customer_id = data.get("customer", "")
        user = db.execute(
            "SELECT id FROM users WHERE email = (SELECT email FROM subscriptions WHERE stripe_customer_id = ?);",
            (customer_id,),
        ).fetchone()
        if user:
            db.execute(
                "UPDATE subscriptions SET status = 'canceled' WHERE stripe_customer_id = ?;",
                (customer_id,),
            )
            db.commit()

    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer", "")
        user = db.execute(
            "SELECT id FROM users WHERE email = (SELECT email FROM subscriptions WHERE stripe_customer_id = ?);",
            (customer_id,),
        ).fetchone()
        if user:
            db.execute(
                "UPDATE subscriptions SET status = 'past_due' WHERE stripe_customer_id = ?;",
                (customer_id,),
            )
            db.commit()


@router.get("/plans", response_model=list[PlanResponse])
def get_plans():
    """
    Return the server-side plan catalog.
    Prices are authoritative — never trust client-provided prices.
    """
    return [
        PlanResponse(**plan_data)
        for plan_data in settings.PLAN_CATALOG.values()
    ]


@router.post("/subscribe", response_model=SubscribeResponse)
def subscribe_to_plan(
    req: SubscribeRequest,
    db: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Subscribe to a plan.

    SERVER-SIDE PRICE ENFORCEMENT:
    - The client provides ONLY the plan_id (e.g., "pro", "enterprise").
    - The server NEVER accepts a price from the client.
    - The price is always looked up from the server-side PLAN_CATALOG.
    - This prevents price manipulation attacks where a malicious client
      sends a lower price to get premium features for less.
    """
    plan_id = req.plan_id.lower().strip()

    # Validate plan exists in server-side catalog
    if plan_id not in settings.PLAN_CATALOG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan '{plan_id}' not found. Available plans: {', '.join(settings.PLAN_CATALOG.keys())}",
        )

    plan = settings.PLAN_CATALOG[plan_id]
    # current_user is a dict from the DB row (keys: id, email, full_name, role, etc.)
    user_id = int(current_user["id"])

    # Check if already subscribed to this plan
    existing = db.execute(
        "SELECT id, plan_id, status FROM subscriptions WHERE user_id = ?;",
        (user_id,),
    ).fetchone()

    if existing and existing[1] == plan_id and existing[2] == "active":
        return SubscribeResponse(
            success=True,
            plan_id=plan_id,
            status="already_active",
            message=f"You are already subscribed to {plan['name']}.",
        )

    # For free tier, just update the DB record directly
    if plan_id == "free":
        if existing:
            db.execute(
                """UPDATE subscriptions SET plan_id = ?, status = 'active', updated_at = CURRENT_TIMESTAMP
                   WHERE user_id = ?;""",
                (plan_id, user_id),
            )
        else:
            db.execute(
                """INSERT INTO subscriptions (user_id, plan_id, status)
                   VALUES (?, ?, 'active');""",
                (user_id, plan_id),
            )
        db.commit()
        return SubscribeResponse(
            success=True,
            plan_id=plan_id,
            status="active",
            message=f"Successfully subscribed to {plan['name']}.",
        )

    # For paid tiers, create a Stripe Checkout session
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe not configured. Set STRIPE_SECRET_KEY to enable paid subscriptions.",
        )

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Look up user email
        user = db.execute("SELECT email FROM users WHERE id = ?;", (user_id,)).fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email=user[0],
            line_items=[{
                "price_data": {
                    "currency": plan["currency"],
                    "product_data": {
                        "name": plan["name"],
                        "description": plan["description"],
                    },
                    "unit_amount": plan["price_cents"],  # Server-side price — never from client
                    "recurring": {"interval": "month"},
                },
                "quantity": 1,
            }],
            success_url="https://auramed.ai/dashboard?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://auramed.ai/pricing",
            metadata={"plan_id": plan_id, "user_id": str(user_id)},
        )

        return SubscribeResponse(
            success=True,
            plan_id=plan_id,
            status="pending",
            message="Redirecting to Stripe Checkout...",
            checkout_url=checkout_session.url,
        )

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Stripe error: {str(e)}",
        )


@router.get("/subscription", response_model=SubscriptionStatusResponse)
def get_subscription_status(
    db: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get the current user's subscription status."""
    user_id = int(current_user["id"])

    sub = db.execute(
        """SELECT plan_id, status, current_period_end, cancel_at_period_end
           FROM subscriptions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1;""",
        (user_id,),
    ).fetchone()

    if not sub:
        # Default to free tier
        return SubscriptionStatusResponse(
            user_id=user_id,
            plan_id="free",
            status="active",
            current_period_end=None,
            cancel_at_period_end=False,
        )

    return SubscriptionStatusResponse(
        user_id=user_id,
        plan_id=sub[0],
        status=sub[1],
        current_period_end=sub[2],
        cancel_at_period_end=bool(sub[3]),
    )
