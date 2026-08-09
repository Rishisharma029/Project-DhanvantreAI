import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.evidence_citation_engine import (
    search_multi_tier_evidence, execute_evidence_citation_engine
)
from app.schemas.evidence_schema import EvidenceCitationRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_search_multi_tier_evidence():
    """Test searching 4 evidence tiers for query tokens."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    citations = search_multi_tier_evidence(["paracetamol", "fever", "pneumonia"], conn)
    conn.close()

    assert len(citations) >= 2
    tiers = [c.source_tier for c in citations]
    assert any(t in ("DRUG_DATABASE", "CLINICAL_GUIDELINE", "DRUG_INTERACTION", "MEDICAL_LITERATURE") for t in tiers)

def test_strict_evidence_enforcement():
    """Test that unsupported claims are flagged with [UNVERIFIED_STATEMENT] under strict enforcement."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = EvidenceCitationRequest(
        medical_query="Pneumonia treatment",
        proposed_explanation="Amoxicillin is recommended for pneumonia. Alien space dust cures fever.",
        enforce_strict_grounding=True
    )
    res = execute_evidence_citation_engine(req, conn)
    conn.close()

    assert res.contains_unsupported_statements is True
    assert len(res.cited_statements) == 2

    # Second statement should be marked unsupported
    second_stmt = res.cited_statements[1]
    assert "[UNVERIFIED_STATEMENT]" in second_stmt.statement
    assert second_stmt.is_supported is False

def test_evidence_api_endpoints():
    """Test /api/v1/evidence/cite and /api/v1/evidence/verify-statement HTTP API endpoints."""
    payload = {
        "medical_query": "Paracetamol with Warfarin interactions",
        "proposed_explanation": "Paracetamol is an analgesic. Warfarin has interaction risks.",
        "enforce_strict_grounding": True
    }
    response = client.post(f"{settings.API_V1_STR}/evidence/cite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "groundness_score" in data
    assert "cited_statements" in data

    single_response = client.post(
        f"{settings.API_V1_STR}/evidence/verify-statement?statement=Paracetamol%20reduces%20fever&medical_query=Paracetamol"
    )
    assert single_response.status_code == 200
    single_data = single_response.json()
    assert "statement" in single_data
