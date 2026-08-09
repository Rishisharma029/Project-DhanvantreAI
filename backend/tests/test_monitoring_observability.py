import os
import sys
import time
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.services.monitoring_service import metrics_registry, track_ai_pipeline_timing, track_rag_retrieval_timing

client = TestClient(app)

def test_health_endpoint():
    """Verify /health endpoint returns comprehensive component status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["healthy", "degraded"]
    assert "timestamp" in data
    assert "components" in data
    assert data["components"]["database"] == "healthy"
    assert data["components"]["cache"] == "healthy"
    assert data["components"]["ai_engine"] == "healthy"

def test_ready_endpoint():
    """Verify /ready Kubernetes readiness probe."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"

def test_live_endpoint():
    """Verify /live Kubernetes liveness probe."""
    response = client.get("/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data

def test_prometheus_metrics_endpoint():
    """Verify /metrics endpoint returns Prometheus formatted metrics."""
    # Send request to record HTTP metric
    client.get("/health")

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    text = response.text
    assert "# HELP http_requests_total" in text
    assert "# HELP http_request_duration_seconds_avg" in text
    assert "# HELP system_health_status" in text
    assert 'system_health_status{component="database"} 1' in text

def test_timing_context_managers():
    """Verify AI pipeline and RAG retrieval timing context managers."""
    with track_ai_pipeline_timing("test_reasoning_pipeline"):
        time.sleep(0.01)

    with track_rag_retrieval_timing("hybrid_vector_bm25", top_k=10):
        time.sleep(0.01)

    metrics_text = metrics_registry.generate_prometheus_metrics()
    assert "ai_pipeline_duration_seconds_avg" in metrics_text
    assert "test_reasoning_pipeline" in metrics_text
    assert "rag_retrieval_duration_seconds_avg" in metrics_text
    assert "hybrid_vector_bm25" in metrics_text
