import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db, get_db
from app.services.advanced_rag_engine import (
    detect_intent, rewrite_and_expand_query, run_advanced_rag_pipeline
)
from app.schemas.rag_schema import RAGQueryRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_rag_intent_detection():
    """Test clinical intent detection logic."""
    assert detect_intent("What are the side effects of Warfarin with Aspirin?") == "DRUG_INTERACTION"
    assert detect_intent("High fever and headache symptoms diagnosis") == "SYMPTOM_DIAGNOSIS"
    assert detect_intent("What is the proper dosage for Paracetamol 650mg?") == "DOSAGE_SAFETY"
    assert detect_intent("Tell me about Acute Coronary Syndrome disease ICD code") == "DISEASE_EXPLORATION"

def test_rag_query_rewriting():
    """Test synonym expansion and multi-query variation generation."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    rewritten, synonyms = rewrite_and_expand_query("fever paracetamol", conn)
    conn.close()

    assert len(rewritten) == 3
    assert isinstance(synonyms, list)

def test_rag_full_pipeline_execution():
    """Test full 6-stage Advanced RAG pipeline execution."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = RAGQueryRequest(query="Paracetamol for fever and headache", max_chunks=10)
    res = run_advanced_rag_pipeline(req, conn)
    conn.close()

    assert res.query == "Paracetamol for fever and headache"
    assert res.detected_intent in ("SYMPTOM_DIAGNOSIS", "DOSAGE_SAFETY", "DRUG_INTERACTION", "DISEASE_EXPLORATION", "GENERAL_MEDICAL_QUERY")
    assert len(res.top_10_evidence) <= 10
    assert res.compressed_context != ""
    assert res.synthesized_answer != ""

def test_rag_api_endpoints():
    """Test /api/v1/rag/query and /api/v1/rag/explain-context HTTP API endpoints."""
    payload = {
        "query": "Amoxicillin side effects and interactions",
        "max_chunks": 10,
        "enable_compression": True
    }
    response = client.post(f"{settings.API_V1_STR}/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "top_10_evidence" in data
    assert "compressed_context" in data

    exp_response = client.post(f"{settings.API_V1_STR}/rag/explain-context", json=payload)
    assert exp_response.status_code == 200
    exp_data = exp_response.json()
    assert "top_10_evidence_chunks" in exp_data
