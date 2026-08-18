"""
Payment / Subscription Schemas for AuraMed AI.
Prices are ALWAYS server-side enforced — never trust client-provided prices.
"""
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List


class PlanResponse(BaseModel):
    """Public plan catalog response (prices from server-side PLAN_CATALOG only)."""
    id: str
    name: str
    description: str
    price_cents: int
    currency: str
    features: List[str]


class SubscribeRequest(BaseModel):
    """
    Subscribe to a plan. The client provides ONLY the plan_id.
    The server looks up the price from PLAN_CATALOG — client price is IGNORED.
    """
    plan_id: str = Field(..., json_schema_extra={"example": "pro"})


class SubscribeResponse(BaseModel):
    """Response after subscription creation."""
    success: bool
    plan_id: str
    status: str
    message: str
    checkout_url: Optional[str] = None  # Stripe Checkout URL if applicable


class WebhookResponse(BaseModel):
    """Response from webhook processing."""
    received: bool
    event_type: str


class SubscriptionStatusResponse(BaseModel):
    """Current subscription status for the authenticated user."""
    user_id: int
    plan_id: str
    status: str
    current_period_end: Optional[str] = None
    cancel_at_period_end: bool = False
