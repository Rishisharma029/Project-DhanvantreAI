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

EXPLAIN_DIS_ID = 995511
EXPLAIN_MED_ID = 995522

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        # Setup Disease
        cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?;", (EXPLAIN_DIS_ID,))
        cursor.execute("DELETE FROM diseases WHERE id = ?;", (EXPLAIN_DIS_ID,))
        cursor.execute("""
            INSERT INTO diseases (id, name, severity_level, description)
            VALUES (?, 'Dengue Fever Explain Test', 'Severe', 'Mosquito-borne viral infection causing high fever');
        """, (EXPLAIN_DIS_ID,))
        
        cursor.execute("INSERT OR IGNORE INTO symptoms (name) VALUES ('high fever');")
        cursor.execute("INSERT OR IGNORE INTO symptoms (name) VALUES ('joint pain');")
        cursor.execute("SELECT id FROM symptoms WHERE name = 'high fever' LIMIT 1;")
        sym1_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM symptoms WHERE name = 'joint pain' LIMIT 1;")
        sym2_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?);", (EXPLAIN_DIS_ID, sym1_id))
        cursor.execute("INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?);", (EXPLAIN_DIS_ID, sym2_id))

        # Setup Medicine
        cursor.execute("DELETE FROM medicine_uses WHERE medicine_id = ?;", (EXPLAIN_MED_ID,))
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (EXPLAIN_MED_ID,))
        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (995522, 'Cipla Ltd');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (?, 'Paracetamol 650mg Explain Tablet', 'Paracetamol 650mg Explain Tablet', 'Paracetamol', 'paracetamol 650mg explain tablet', 20.00, 'Paracetamol (650mg)', 995522);
        """, (EXPLAIN_MED_ID,))
        cursor.execute("INSERT INTO medicine_uses (medicine_id, use_name) VALUES (?, 'Dengue Fever Explain Test');", (EXPLAIN_MED_ID,))

        conn.commit()
    finally:
        conn.close()

def test_explainability_all_5_pillars():
    payload = {
        "disease_name": "Dengue Fever Explain Test",
        "medicine_name": "Paracetamol 650mg Explain Tablet",
        "reported_symptoms": ["high fever"],
        "confidence_score": 0.88
    }
    response = client.post("/api/v1/explainability/explain", json=payload)
    assert response.status_code == 200
    data = response.json()

    # 1. Why Disease?
    assert "Dengue Fever Explain Test" in data["why_disease"]
    assert "high fever" in data["why_disease"].lower()

    # 2. Why Medicine?
    assert "Paracetamol 650mg Explain Tablet" in data["why_medicine"]

    # 3. Why Confidence?
    assert data["why_confidence"]["confidence_score"] == 0.88
    assert "88%" in data["why_confidence"]["confidence_percentage"]
    assert "Formula" in data["why_confidence"]["formula"] or "Sensitivity" in data["why_confidence"]["formula"]

    # 4. Alternative Diseases
    assert len(data["alternative_diseases"]) > 0
    assert data["alternative_diseases"][0]["disease_name"] is not None

    # 5. Missing Symptoms
    assert isinstance(data["missing_symptoms"], list)
    assert "disclaimer" in data
