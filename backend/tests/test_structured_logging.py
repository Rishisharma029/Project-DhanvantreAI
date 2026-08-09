import os
import sys
import json
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.services.structured_logging_service import sanitize_phi, StructuredLogger

client = TestClient(app)

def test_phi_sanitization():
    """Verify PHI and sensitive credentials redaction in log payloads."""
    raw_text = 'User email john.doe@med.org with SSN 123-45-6789 and "password": "secret123" for "patient_name": "Jane Smith"'
    sanitized = sanitize_phi(raw_text)

    assert "[REDACTED_EMAIL]" in sanitized
    assert "[REDACTED_SSN]" in sanitized
    assert '"password": "[REDACTED]"' in sanitized
    assert '"patient_name": "[REDACTED_PHI]"' in sanitized
    assert "john.doe@med.org" not in sanitized
    assert "123-45-6789" not in sanitized
    assert "Jane Smith" not in sanitized

def test_structured_logger_methods():
    """Verify StructuredLogger methods execute cleanly without throwing errors."""
    corr_id = "CORR-TEST-1234"

    # 1. API Log
    StructuredLogger.log_api_request("GET", "/api/v1/health", 200, 12.5, corr_id)

    # 2. Recommendation Log
    StructuredLogger.log_recommendation_event(disease_id=5, top_medicines_count=3, confidence_score=0.92, correlation_id=corr_id)

    # 3. AI Reasoning Log
    StructuredLogger.log_ai_reasoning_event("differential_reasoning", rule_in_count=4, rule_out_count=2, execution_time_ms=45.2, correlation_id=corr_id)

    # 4. Error Log
    StructuredLogger.log_error("DATABASE_TIMEOUT", "Connection to DB timed out after 5000ms", stack_trace="Traceback...", correlation_id=corr_id)

def test_correlation_id_in_middleware():
    """Verify HTTP requests carry and return X-Correlation-ID headers."""
    custom_corr = "CUSTOM-CORR-999"
    response = client.get("/health", headers={"X-Correlation-ID": custom_corr})
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") == custom_corr

    # Test auto-generated correlation ID
    auto_res = client.get("/health")
    assert auto_res.status_code == 200
    assert "X-Correlation-ID" in auto_res.headers
    assert auto_res.headers["X-Correlation-ID"].startswith("CORR-")
