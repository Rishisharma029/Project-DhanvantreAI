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
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO symptoms (id, name, severity_weight) VALUES (1, 'fever', 2), (2, 'headache', 1), (3, 'body pain', 2);")
    cursor.execute("INSERT OR IGNORE INTO diseases (id, name, severity_level, description) VALUES (1, 'Influenza', 'Moderate', 'Flu infection');")
    cursor.execute("INSERT OR IGNORE INTO disease_symptoms (disease_id, symptom_id) VALUES (1, 1), (1, 2);")
    conn.commit()
    conn.close()

def test_emergency_red_flag_detection():
    payload = {
        "reported_symptoms": ["chest pain", "fever"]
    }
    response = client.post("/api/v1/adaptive-questions/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_emergency"] is True
    assert data["should_continue"] is False
    assert "CRITICAL EMERGENCY" in data["emergency_warning"]
    assert data["next_question"] is None

def test_followup_question_generation_sequence():
    # Turn 0: Initial symptom 'fever'
    p0 = {
        "reported_symptoms": ["fever"],
        "answered_turns": []
    }
    r0 = client.post("/api/v1/adaptive-questions/evaluate", json=p0).json()
    
    assert r0["is_emergency"] is False
    assert r0["should_continue"] is True
    assert r0["next_question"]["question_id"] == "q_duration"
    assert "How long" in r0["next_question"]["question_text"]

def test_confidence_progression_and_threshold_termination():
    # Simulate multi-turn Q&A
    p_multi = {
        "reported_symptoms": ["fever", "headache"],
        "answered_turns": [
            {"question_id": "q_duration", "question_text": "How long?", "answer": "2 days"},
            {"question_id": "q_temperature", "question_text": "Temperature?", "answer": "High (> 101.5°F)"},
            {"question_id": "q_body_pain", "question_text": "Body Pain?", "answer": "Yes, severe body pain"}
        ],
        "confidence_threshold": 0.85
    }
    res = client.post("/api/v1/adaptive-questions/evaluate", json=p_multi).json()

    assert res["confidence_score"] >= 0.85
    assert res["enough_information"] is True
    assert res["should_continue"] is False
    assert res["next_question"] is None
    assert "Confidence threshold reached" in res["termination_reason"]

def test_max_question_limit_termination():
    p_max = {
        "reported_symptoms": ["fever"],
        "answered_turns": [
            {"question_id": "q_duration", "question_text": "How long?", "answer": "1 day"},
            {"question_id": "q_temperature", "question_text": "Temperature?", "answer": "Normal"},
            {"question_id": "q_body_pain", "question_text": "Body pain?", "answer": "None"},
            {"question_id": "q_nausea_vomiting", "question_text": "Nausea?", "answer": "None"}
        ],
        "max_questions": 4,
        "confidence_threshold": 0.99
    }
    res = client.post("/api/v1/adaptive-questions/evaluate", json=p_max).json()

    assert res["enough_information"] is True
    assert res["should_continue"] is False
    assert "Maximum question limit reached" in res["termination_reason"]
