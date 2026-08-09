import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
client = TestClient(app)

def test_openapi_documentation_endpoints():
    """Verify OpenAPI 3.1 schema, Swagger UI (/docs), and Redoc (/redoc) endpoints."""
    # 1. Swagger UI
    res_docs = client.get("/docs")
    assert res_docs.status_code == 200
    assert "text/html" in res_docs.headers["content-type"]

    # 2. Redoc UI
    res_redoc = client.get("/redoc")
    assert res_redoc.status_code == 200
    assert "text/html" in res_redoc.headers["content-type"]

    # 3. OpenAPI JSON Schema
    res_openapi = client.get("/api/v1/openapi.json")
    assert res_openapi.status_code == 200
    data = res_openapi.json()
    assert "openapi" in data
    assert "paths" in data
    assert "/api/v1/performance/stats" in data["paths"]

def test_performance_dashboard_api():
    """Verify /api/v1/performance/stats telemetry API."""
    response = client.get("/api/v1/performance/stats")
    assert response.status_code == 200
    data = response.json()
    assert "throughput" in data
    assert "system_resources" in data
    assert "latency" in data
    assert "cache" in data

    assert "requests_per_second" in data["throughput"]
    assert "cpu_utilization_percent" in data["system_resources"]
    assert "memory_usage_mb" in data["system_resources"]
    assert "p95_ms" in data["latency"]
    assert "hit_rate_percent" in data["cache"]

def test_performance_dashboard_web_page():
    """Verify frontend performance dashboard page routes."""
    res_html = client.get("/performance.html")
    assert res_html.status_code == 200
    assert "text/html" in res_html.headers["content-type"]
    assert "AuraMed AI — Live Performance Telemetry" in res_html.text

def test_documentation_suite_files_exist():
    """Verify complete documentation suite markdown files exist."""
    doc_files = [
        "README.md",
        "docs/ARCHITECTURE.md",
        "docs/ER_DIAGRAM.md",
        "docs/API_GUIDE.md",
        "docs/DEPLOYMENT_GUIDE.md",
        "docs/SECURITY_GUIDE.md",
        "docs/AI_DESIGN.md"
    ]
    for rel_path in doc_files:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        assert os.path.exists(full_path), f"Documentation file missing: {rel_path}"
