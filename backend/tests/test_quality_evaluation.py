import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.services.quality_evaluation_engine import evaluate_ai_quality
from app.schemas.quality_evaluation_schema import QualityEvaluationRequest, QualityGrade

client = TestClient(app)

def test_high_quality_response_evaluation():
    """Verify that a faithful, grounded, cited, and safe response receives high quality scores."""
    req = QualityEvaluationRequest(
        query="Paracetamol dosage for fever",
        ai_response_text="Paracetamol 500mg every 6 hours is indicated for fever relief. Consult doctor for persistent fever. [WHO Guidelines Sec 4.2]",
        retrieved_context_chunks=["Paracetamol 500mg every 6 hours is indicated for fever relief. Consult doctor for persistent fever."],
        citations=["WHO Guidelines Sec 4.2"]
    )
    res = evaluate_ai_quality(req)


    assert res.overall_quality_score >= 80.0
    assert res.quality_grade in (QualityGrade.EXCELLENT, QualityGrade.GOOD)
    assert res.is_approved_for_delivery is True
    assert len(res.metrics) == 5
    assert "Faithfulness" in res.metrics
    assert "Groundedness" in res.metrics
    assert "Citation Coverage" in res.metrics
    assert "Consistency" in res.metrics
    assert "Safety" in res.metrics

def test_low_citation_and_ungrounded_response():
    """Verify that ungrounded or uncited text triggers remediation recommendations."""
    req = QualityEvaluationRequest(
        query="Unrelated medical query",
        ai_response_text="Some random text without citations or clear medical backing.",
        retrieved_context_chunks=["Completely different context content about cardiac care."],
        citations=[]
    )
    res = evaluate_ai_quality(req)

    assert res.overall_quality_score < 75.0
    assert len(res.recommended_remediations) >= 1

def test_quality_evaluation_api_endpoint():
    """Test HTTP POST /api/v1/quality/evaluate REST endpoint."""
    payload = {
        "query": "Amoxicillin indication",
        "ai_response_text": "Amoxicillin is a broad-spectrum penicillin antibiotic for bacterial infection. [FDA Monograph]",
        "retrieved_context_chunks": ["Amoxicillin is an antibiotic for bacterial infections."],
        "citations": ["FDA Monograph"]
    }
    response = client.post(f"{settings.API_V1_STR}/quality/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "overall_quality_score" in data
    assert "quality_grade" in data
    assert "metrics" in data
    assert "Faithfulness" in data["metrics"]
