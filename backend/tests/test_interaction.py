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
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        # Seed test pair if not present
        cursor.execute("SELECT id FROM drug_interactions WHERE LOWER(drug_a_name) LIKE '%aspirin%' AND LOWER(drug_b_name) LIKE '%warfarin%' LIMIT 1;")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO drug_interactions (drug_a_name, drug_b_name, severity, severity_tag, interaction_description)
                VALUES ('Aspirin', 'Warfarin', 'Major', '🔴 Dangerous', 'Concurrent use increases risk of severe bleeding.');
            """)
            conn.commit()
    finally:
        conn.close()

def test_pairwise_drug_interaction_major():
    payload = {
        "drug_a": "Aspirin",
        "drug_b": "Warfarin"
    }
    response = client.post("/api/v1/interactions/check-pair", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["has_interactions"] is True
    assert data["highest_severity"] in ["Major", "Moderate"]
    assert len(data["interactions"]) > 0
    item = data["interactions"][0]
    assert "🔴" in item["severity_icon"] or "🟡" in item["severity_icon"]

def test_pairwise_safe_drugs():
    payload = {
        "drug_a": "NonExistentDrug12345",
        "drug_b": "NonExistentDrug67890"
    }
    response = client.post("/api/v1/interactions/check-pair", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["has_interactions"] is False
    assert data["highest_severity"] == "Safe"

def test_regimen_polypharmacy_check():
    payload = {
        "medicines": ["Aspirin", "Warfarin"]
    }
    response = client.post("/api/v1/interactions/check-regimen", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["has_interactions"] is True
    assert data["total_interactions_found"] >= 1

def test_current_vs_recommended_cross_checker():
    payload = {
        "current_medicines": ["Warfarin"],
        "recommended_medicines": ["Aspirin"]
    }
    response = client.post("/api/v1/interactions/check-current-vs-recommended", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["has_conflicts"] is True
    assert data["total_conflicts_found"] >= 1
