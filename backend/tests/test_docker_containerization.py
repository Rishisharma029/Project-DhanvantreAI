import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def test_dockerfile_multi_stage_structure():
    """Verify backend and frontend Dockerfiles employ Multi-Stage Builds."""
    backend_df = os.path.join(PROJECT_ROOT, "backend", "Dockerfile")
    frontend_df = os.path.join(PROJECT_ROOT, "frontend", "Dockerfile")

    assert os.path.exists(backend_df), "backend/Dockerfile missing"
    assert os.path.exists(frontend_df), "frontend/Dockerfile missing"

    with open(backend_df, "r", encoding="utf-8") as f:
        b_content = f.read()
        assert "AS builder" in b_content
        assert "AS runner" in b_content
        assert "HEALTHCHECK" in b_content

    with open(frontend_df, "r", encoding="utf-8") as f:
        f_content = f.read()
        assert "AS builder" in f_content
        assert "AS runner" in f_content
        assert "nginx" in f_content

def test_docker_compose_services():
    """Verify docker-compose.yml configures PostgreSQL, Redis, Backend, Frontend, and Nginx."""
    compose_path = os.path.join(PROJECT_ROOT, "docker-compose.yml")
    assert os.path.exists(compose_path), "docker-compose.yml missing"

    with open(compose_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "postgres:" in content
        assert "redis:" in content
        assert "backend:" in content
        assert "frontend:" in content
        assert "nginx:" in content
        assert "auramed_network" in content
        assert "healthcheck:" in content

def test_nginx_conf_routing_and_security():
    """Verify Nginx reverse proxy configuration includes API proxying, rate limiting, and security headers."""
    nginx_conf = os.path.join(PROJECT_ROOT, "nginx", "nginx.conf")
    assert os.path.exists(nginx_conf), "nginx/nginx.conf missing"

    with open(nginx_conf, "r", encoding="utf-8") as f:
        n_content = f.read()
        assert "upstream backend_service" in n_content
        assert "upstream frontend_service" in n_content
        assert "limit_req_zone" in n_content
        assert "X-Frame-Options" in n_content
        assert "X-Content-Type-Options" in n_content
        assert "Strict-Transport-Security" in n_content
        assert "location /api/" in n_content
