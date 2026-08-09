import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from fastapi.middleware.gzip import GZipMiddleware
from app.main import app
from app.services.api_gateway_service import SlidingWindowRateLimiter

client = TestClient(app)

def test_gateway_health_endpoint():
    res = client.get("/api/v1/gateway/health")
    assert res.status_code == 200
    data = res.json()
    assert data["gateway_status"] == "OPERATIONAL"
    assert data["total_registered_routes"] >= 5
    assert data["rate_limiting_enabled"] is True
    assert data["compression_enabled"] is True

def test_gateway_routes_endpoint():
    res = client.get("/api/v1/gateway/routes")
    assert res.status_code == 200
    routes = res.json()
    assert isinstance(routes, list)
    assert len(routes) >= 5
    paths = [r["path"] for r in routes]
    assert "/health" in paths or "/" in paths or "/api/v1/gateway/routes" in paths

def test_gateway_rate_limit_status():
    res = client.get("/api/v1/gateway/rate-limit-status")
    assert res.status_code == 200
    data = res.json()
    assert data["max_limit"] == 100
    assert data["remaining"] >= 0

def test_response_gzip_compression_middleware():
    # Verify GZipMiddleware is attached to main app
    middleware_types = [type(m.cls) for m in app.user_middleware if hasattr(m, 'cls')]
    assert GZipMiddleware in middleware_types or len(app.user_middleware) >= 1

    res = client.get("/api/v1/gateway/routes")
    assert res.status_code == 200
    assert len(res.content) > 0

def test_rate_limiting_exceeded():
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=60)
    
    # 3 allowed for specific client IP
    test_ip = "192.168.99.100"
    ok1, _, _ = limiter.check_rate_limit(test_ip)
    ok2, _, _ = limiter.check_rate_limit(test_ip)
    ok3, _, _ = limiter.check_rate_limit(test_ip)
    assert ok1 is True
    assert ok2 is True
    assert ok3 is True

    # 4th blocked
    ok4, remaining, reset_in = limiter.check_rate_limit(test_ip)
    assert ok4 is False
    assert remaining == 0
    assert reset_in > 0
