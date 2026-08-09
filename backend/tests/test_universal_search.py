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

UNI_MED_ID = 994411
UNI_DIS_ID = 994422

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (UNI_MED_ID,))
        cursor.execute("DELETE FROM diseases WHERE id = ?;", (UNI_DIS_ID,))
        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (994411, 'Sun Pharma Universal');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (?, 'Universal FeverRelief 500mg', 'Universal FeverRelief', 'Paracetamol', 'universal feverrelief 500mg', 30.00, 'Paracetamol (500mg)', 994411);
        """, (UNI_MED_ID,))
        cursor.execute("""
            INSERT INTO diseases (id, name, severity_level, description)
            VALUES (?, 'Universal Viral Fever Test', 'Moderate', 'Viral infection causing acute high fever and body ache');
        """, (UNI_DIS_ID,))
        cursor.execute("INSERT OR IGNORE INTO symptoms (name) VALUES ('universal high fever');")
        cursor.execute("INSERT OR IGNORE INTO medicine_ingredients (medicine_id, ingredient_name) VALUES (?, 'Paracetamol Ingredient');", (UNI_MED_ID,))

        conn.commit()
    finally:
        conn.close()

def test_universal_search_all_domains():
    response = client.get("/api/v1/search/universal?q=Fever")
    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "Fever"
    assert data["total_results"] > 0
    assert "Medicine" in data["categories_found"] or "Disease" in data["categories_found"]

def test_universal_search_paracetamol():
    response = client.get("/api/v1/search/universal?q=Paracetamol")
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0
    assert "Medicine" in data["categories_found"]

def test_universal_search_manufacturer():
    response = client.get("/api/v1/search/universal?q=Sun%20Pharma")
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0
    assert "Manufacturer" in data["categories_found"]

def test_universal_search_domain_filter():
    response = client.get("/api/v1/search/universal?q=Fever&domain=diseases")
    assert response.status_code == 200
    data = response.json()

    assert data["domain_filter"] == "diseases"
    for cat in data["categories_found"]:
        assert cat == "Disease"
