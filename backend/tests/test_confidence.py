import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.config import settings
from app.main import app

client = TestClient(app)

def test_high_alignment_confidence_calibration():
    payload = {
        "disease_name": "Dengue Fever",
        "base_disease_confidence": 0.90,
        "matched_symptoms_count": 4,
        "total_disease_symptoms_count": 5,
        "interaction_severity": "None",
        "safety_grade": "SAFE",
        "safety_score": 95.0
    }
    response = client.post("/api/v1/confidence/calibrate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["final_confidence_score"] >= 0.85
    assert data["confidence_grade"] == "High Confidence"
    assert data["signal_breakdown"]["high_alignment_bonus"] == 0.05

def test_interaction_penalty_confidence_calibration():
    payload = {
        "disease_name": "Hypertension",
        "base_disease_confidence": 0.80,
        "matched_symptoms_count": 3,
        "total_disease_symptoms_count": 4,
        "interaction_severity": "Major",
        "safety_grade": "SAFE",
        "safety_score": 80.0
    }
    response = client.post("/api/v1/confidence/calibrate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["signal_breakdown"]["interaction_penalty"] == 0.30
    assert data["final_confidence_score"] < 0.80

def test_contraindication_penalty_confidence_calibration():
    payload = {
        "disease_name": "Pneumonia",
        "base_disease_confidence": 0.85,
        "matched_symptoms_count": 4,
        "total_disease_symptoms_count": 5,
        "interaction_severity": "None",
        "safety_grade": "CONTRAINDICATED",
        "safety_score": 0.0
    }
    response = client.post("/api/v1/confidence/calibrate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["signal_breakdown"]["contradiction_penalty"] == 0.50
    assert data["confidence_grade"] == "Low Confidence"
