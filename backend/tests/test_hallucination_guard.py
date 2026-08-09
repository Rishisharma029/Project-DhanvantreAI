import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db
from app.services.hallucination_guard_engine import evaluate_hallucination_guard
from app.schemas.hallucination_guard_schema import HallucinationGuardRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_grounded_response_passes():
    """Verify that a response backed by evidence context passes with high grounding score."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = HallucinationGuardRequest(
        llm_response_text="Paracetamol is an antipyretic for fever relief. Rest and hydration support recovery.",
        context_evidence_chunks=[
            "Paracetamol is an antipyretic drug indicated for fever relief.",
            "Bed rest and hydration support patient recovery during fever."
        ]
    )
    res = evaluate_hallucination_guard(req, conn)
    conn.close()

    assert res.is_safe is True
    assert res.hallucination_detected is False
    assert res.grounding_score >= 80.0
    assert res.action_taken == "PASSED"

def test_hallucinated_claim_detected_and_sanitized():
    """Verify that unsupported or contradicted claims are detected and sanitized."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = HallucinationGuardRequest(
        llm_response_text="Paracetamol helps relieve fever. Amoxicillin cures viral flu instantly.",
        context_evidence_chunks=[
            "Paracetamol is an antipyretic for fever relief.",
            "Viral flu is a viral illness; antibiotics like Amoxicillin are ineffective against viral flu."
        ],
        allow_auto_regeneration=True
    )
    res = evaluate_hallucination_guard(req, conn)
    conn.close()

    assert res.hallucination_detected is True
    assert res.unsupported_claims_count >= 1
    assert res.action_taken == "REGENERATED_AND_SANITIZED"
    assert "[REDACTED_UNVERIFIED_CLAIM" in res.verified_response_text

def test_hallucination_guard_api_endpoint():
    """Test HTTP POST /api/v1/hallucination-guard/audit REST endpoint."""
    payload = {
        "llm_response_text": "Paracetamol 500mg treats fever.",
        "context_evidence_chunks": ["Paracetamol 500mg is an antipyretic for fever."],
        "allow_auto_regeneration": True
    }
    response = client.post(f"{settings.API_V1_STR}/hallucination-guard/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_safe" in data
    assert "grounding_score" in data
    assert "claims" in data
    assert len(data["claims"]) >= 1
