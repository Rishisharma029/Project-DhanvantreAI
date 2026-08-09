import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.clinical_guideline_engine import (
    match_clinical_guidelines, fetch_guidelines_by_authority
)
from app.schemas.guideline_schema import GuidelineMatchRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_guideline_matching():
    """Test clinical guideline matching with section citations."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = GuidelineMatchRequest(condition_name="Pneumonia", reported_symptoms=["fever", "cough"])
    res = match_clinical_guidelines(req, conn)
    conn.close()

    assert res.matched_guidelines_count >= 2
    assert len(res.guideline_references) >= 2

    first = res.guideline_references[0]
    assert first.authority in ("WHO", "CDC", "NICE", "NATIONAL_ICMR", "NATIONAL_FDA")
    assert "Sec" in first.section_reference
    assert first.evidence_grade.startswith("Grade")

def test_authority_filtering():
    """Test filtering clinical guidelines by authority (WHO, CDC, NICE)."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = GuidelineMatchRequest(condition_name="COVID-19", authority_filter="WHO")
    res = match_clinical_guidelines(req, conn)
    conn.close()

    assert res.matched_guidelines_count >= 1
    for item in res.guideline_references:
        assert item.authority == "WHO"

def test_fetch_guidelines_by_authority():
    """Test fetching all guidelines by authority code."""
    who_items = fetch_guidelines_by_authority("WHO")
    assert len(who_items) >= 3
    for item in who_items:
        assert item.authority == "WHO"

def test_guideline_api_endpoints():
    """Test /api/v1/guidelines/match and /api/v1/guidelines/authority/{authority_code} HTTP API endpoints."""
    payload = {
        "condition_name": "Hypertension",
        "reported_symptoms": ["headache"]
    }
    response = client.post(f"{settings.API_V1_STR}/guidelines/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "guideline_references" in data
    assert len(data["guideline_references"]) > 0

    auth_response = client.get(f"{settings.API_V1_STR}/guidelines/authority/NICE")
    assert auth_response.status_code == 200
    auth_data = auth_response.json()
    assert isinstance(auth_data, list)
    assert len(auth_data) > 0
