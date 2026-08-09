import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db
from app.services.personalized_insights_engine import generate_personalized_insights
from app.services.explainability_dashboard_engine import generate_explainability_dashboard
from app.schemas.personalized_insights_schema import PersonalizedInsightsRequest, InsightCategory
from app.schemas.explainability_dashboard_schema import ExplainabilityDashboardRequest, DashboardStep

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_personalized_insights_generation():
    """Verify daily insights are generated across all 4 categories."""
    req = PersonalizedInsightsRequest(
        patient_age=45,
        current_medications=["Paracetamol", "Amlodipine"],
        chronic_conditions=["Hypertension"]
    )
    res = generate_personalized_insights(req)

    assert res.total_insights >= 4
    categories = {insight.category for insight in res.insights}
    expected_categories = {
        InsightCategory.MEDICINE_ADHERENCE,
        InsightCategory.WATER_HYDRATION,
        InsightCategory.LIFESTYLE_SUGGESTION,
        InsightCategory.HEALTH_EDUCATION
    }
    assert expected_categories.issubset(categories)

def test_explainability_dashboard_7_steps():
    """Verify 7-step transparency trajectory (Symptoms -> Disease -> Confidence -> Evidence -> Medicines -> Safety -> Final Explanation)."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = ExplainabilityDashboardRequest(
        reported_symptoms=["fever", "cough", "body pain"],
        suspected_disease="Acute Bronchitis",
        prescribed_medicines=["Amoxicillin", "Paracetamol"]
    )
    res = generate_explainability_dashboard(req, conn)
    conn.close()

    assert res.transparency_score == 100.0
    assert len(res.steps) == 7

    step_names = [s.step_name for s in res.steps]
    expected_steps = [
        DashboardStep.SYMPTOMS,
        DashboardStep.DISEASE,
        DashboardStep.CONFIDENCE,
        DashboardStep.EVIDENCE,
        DashboardStep.MEDICINES,
        DashboardStep.SAFETY,
        DashboardStep.FINAL_EXPLANATION
    ]
    assert step_names == expected_steps

def test_insights_and_explainability_api_endpoints():
    """Test HTTP REST endpoints for Insights and Explainability Dashboard."""
    # 1. Daily Insights Endpoint
    i_res = client.post(f"{settings.API_V1_STR}/insights/daily", json={"patient_age": 30})
    assert i_res.status_code == 200
    i_data = i_res.json()
    assert "insights" in i_data
    assert len(i_data["insights"]) >= 4

    # 2. Explainability Dashboard Endpoint
    d_payload = {
        "reported_symptoms": ["fever", "cough"],
        "suspected_disease": "Pneumonia",
        "prescribed_medicines": ["Azithromycin"]
    }
    d_res = client.post(f"{settings.API_V1_STR}/explainability/dashboard", json=d_payload)
    assert d_res.status_code == 200
    d_data = d_res.json()
    assert "steps" in d_data
    assert len(d_data["steps"]) == 7
