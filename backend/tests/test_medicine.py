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

TEST_MED_ID = 999991

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Ensure clean test medicine insertion
    cursor.execute("DELETE FROM substitutes WHERE medicine_id = ?;", (TEST_MED_ID,))
    cursor.execute("DELETE FROM side_effects WHERE medicine_id = ?;", (TEST_MED_ID,))
    cursor.execute("DELETE FROM medicine_uses WHERE medicine_id = ?;", (TEST_MED_ID,))
    cursor.execute("DELETE FROM medicine_ingredients WHERE medicine_id = ?;", (TEST_MED_ID,))
    cursor.execute("DELETE FROM medicines WHERE id = ?;", (TEST_MED_ID,))

    cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (999991, 'Glaxo SmithKline Test');")
    cursor.execute("""
        INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
        VALUES (?, 'Augmentin 625 Duo Test Tablet', 'Augmentin 625 Duo Test Tablet', 'Amoxycillin + Clavulanic Acid', 'augmentin 625 duo test tablet', 223.42, 'Amoxycillin (500mg) + Clavulanic Acid (125mg)', 999991);
    """, (TEST_MED_ID,))
    cursor.execute("INSERT INTO medicine_ingredients (medicine_id, ingredient_name, strength, unit) VALUES (?, 'Amoxycillin', 500.0, 'mg'), (?, 'Clavulanic Acid', 125.0, 'mg');", (TEST_MED_ID, TEST_MED_ID))
    cursor.execute("INSERT INTO medicine_uses (medicine_id, use_name) VALUES (?, 'Bacterial Infection'), (?, 'Fever');", (TEST_MED_ID, TEST_MED_ID))
    cursor.execute("INSERT INTO side_effects (medicine_id, side_effect_name) VALUES (?, 'Vomiting'), (?, 'Nausea');", (TEST_MED_ID, TEST_MED_ID))
    cursor.execute("INSERT INTO substitutes (medicine_id, substitute_name, substitute_medicine_id) VALUES (?, 'Moxikind-CV 625 Test Tablet', NULL);", (TEST_MED_ID,))
    
    conn.commit()
    conn.close()

def test_medicine_name_and_brand_search():
    response = client.get("/api/v1/medicines/search?q=Augmentin")
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0
    meds = data["medicines"]
    assert any("augmentin" in m["canonical_name"].lower() for m in meds)

def test_medicine_search_by_generic_name():
    response = client.get("/api/v1/medicines/search?q=Amoxycillin&by=generic")
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0
    meds = data["medicines"]
    assert any("amoxycillin" in (m["generic_name"] or "").lower() for m in meds)

def test_medicine_search_by_ingredient():
    response = client.get("/api/v1/medicines/ingredient/Amoxycillin")
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0

def test_medicine_search_by_use():
    response = client.get("/api/v1/medicines/use/Bacterial")
    assert response.status_code == 200
    data = response.json()

    assert data["total_results"] > 0

def test_medicine_details_and_substitutes():
    detail_res = client.get(f"/api/v1/medicines/{TEST_MED_ID}")
    assert detail_res.status_code == 200
    details = detail_res.json()

    assert details["id"] == TEST_MED_ID
    assert "Augmentin" in details["canonical_name"]
    assert details["manufacturer_name"] == "Glaxo SmithKline Test"
    assert len(details["ingredients"]) >= 2
    assert any(ing["ingredient_name"] == "Amoxycillin" for ing in details["ingredients"])
    assert "Bacterial Infection" in details["uses"]
    assert len(details["substitutes"]) > 0

    sub_res = client.get(f"/api/v1/medicines/{TEST_MED_ID}/substitutes")
    assert sub_res.status_code == 200
    subs = sub_res.json()
    assert len(subs) > 0
    assert subs[0]["substitute_name"] == "Moxikind-CV 625 Test Tablet"
