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

KNOW_DIS_ID = 998811
KNOW_MED_ID = 998822

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=10)
    cursor = conn.cursor()
    try:
        # 1. Disease Setup
        cursor.execute("DELETE FROM disease_workouts WHERE disease_id = ?;", (KNOW_DIS_ID,))
        cursor.execute("DELETE FROM disease_precautions WHERE disease_id = ?;", (KNOW_DIS_ID,))
        cursor.execute("DELETE FROM disease_diets WHERE disease_id = ?;", (KNOW_DIS_ID,))
        cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?;", (KNOW_DIS_ID,))
        cursor.execute("DELETE FROM diseases WHERE id = ?;", (KNOW_DIS_ID,))

        cursor.execute("""
            INSERT INTO diseases (id, name, severity_level, description)
            VALUES (?, 'Dengue Fever Test', 'Severe', 'Mosquito-borne viral infection');
        """, (KNOW_DIS_ID,))
        
        cursor.execute("INSERT OR IGNORE INTO symptoms (name) VALUES ('high fever test');")
        cursor.execute("SELECT id FROM symptoms WHERE name = 'high fever test' LIMIT 1;")
        sym_id = cursor.fetchone()[0]
        
        cursor.execute("INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?);", (KNOW_DIS_ID, sym_id))
        cursor.execute("INSERT INTO disease_diets (disease_id, diet) VALUES (?, 'Papaya leaf extract and high hydration');", (KNOW_DIS_ID,))
        cursor.execute("INSERT INTO disease_precautions (disease_id, precaution) VALUES (?, 'Use mosquito repellent nets');", (KNOW_DIS_ID,))
        cursor.execute("INSERT INTO disease_workouts (disease_id, workout) VALUES (?, 'Complete bed rest; avoid strenuous exercise');", (KNOW_DIS_ID,))

        # 2. Medicine Setup
        cursor.execute("DELETE FROM substitutes WHERE medicine_id = ?;", (KNOW_MED_ID,))
        cursor.execute("DELETE FROM medicine_uses WHERE medicine_id = ?;", (KNOW_MED_ID,))
        cursor.execute("DELETE FROM side_effects WHERE medicine_id = ?;", (KNOW_MED_ID,))
        cursor.execute("DELETE FROM medicine_ingredients WHERE medicine_id = ?;", (KNOW_MED_ID,))
        cursor.execute("DELETE FROM medicines WHERE id = ?;", (KNOW_MED_ID,))

        cursor.execute("INSERT OR IGNORE INTO manufacturers (id, name) VALUES (998822, 'GSK Test');")
        cursor.execute("""
            INSERT INTO medicines (id, canonical_name, brand_name, generic_name, canonical_key, price_inr, composition, manufacturer_id)
            VALUES (?, 'Augmentin 625 Knowledge Tablet', 'Augmentin 625 Knowledge Tablet', 'Amoxycillin + Clavulanic Acid', 'augmentin 625 knowledge tablet', 200.00, 'Amoxycillin (500mg) + Clavulanic Acid (125mg)', 998822);
        """, (KNOW_MED_ID,))
        cursor.execute("INSERT INTO medicine_ingredients (medicine_id, ingredient_name, strength, unit) VALUES (?, 'Amoxycillin', 500.0, 'mg');", (KNOW_MED_ID,))
        cursor.execute("INSERT INTO side_effects (medicine_id, side_effect_name, frequency) VALUES (?, 'Diarrhea', 'Common');", (KNOW_MED_ID,))
        cursor.execute("INSERT INTO medicine_uses (medicine_id, use_name) VALUES (?, 'Bacterial Infection');", (KNOW_MED_ID,))
        cursor.execute("INSERT INTO substitutes (medicine_id, substitute_name) VALUES (?, 'Moxikind-CV Knowledge Tablet');", (KNOW_MED_ID,))

        conn.commit()
    finally:
        conn.close()

def test_disease_360_knowledge_retrieval():
    response = client.get(f"/api/v1/knowledge/disease/{KNOW_DIS_ID}")
    assert response.status_code == 200
    data = response.json()

    assert data["disease_name"] == "Dengue Fever Test"
    assert data["severity_level"] == "Severe"
    assert len(data["symptoms"]) > 0
    assert len(data["diets"]) > 0
    assert "Papaya" in data["diets"][0]
    assert len(data["precautions"]) > 0
    assert len(data["workouts"]) > 0

def test_medicine_360_knowledge_retrieval():
    response = client.get(f"/api/v1/knowledge/medicine/{KNOW_MED_ID}")
    assert response.status_code == 200
    data = response.json()

    assert "Augmentin" in data["canonical_name"]
    assert len(data["ingredients"]) > 0
    assert len(data["side_effects"]) > 0
    assert len(data["uses"]) > 0
    assert len(data["substitutes"]) > 0

def test_domain_standalone_fetchers():
    diets_res = client.get("/api/v1/knowledge/diets/Dengue Fever Test")
    assert diets_res.status_code == 200
    assert len(diets_res.json()) > 0

    preca_res = client.get("/api/v1/knowledge/precautions/Dengue Fever Test")
    assert preca_res.status_code == 200
    assert len(preca_res.json()) > 0

    work_res = client.get("/api/v1/knowledge/workouts/Dengue Fever Test")
    assert work_res.status_code == 200
    assert len(work_res.json()) > 0
