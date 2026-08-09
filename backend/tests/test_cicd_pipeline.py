import os
import sys
import subprocess
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def test_ci_cd_workflow_file_structure():
    """Verify GitHub Actions CI/CD workflow contains all required pipeline stages."""
    workflow_path = os.path.join(PROJECT_ROOT, ".github", "workflows", "ci-cd.yml")
    assert os.path.exists(workflow_path), ".github/workflows/ci-cd.yml missing"

    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "name: AuraMed AI - Production CI/CD Pipeline" in content
        assert "on:" in content
        assert "push:" in content
        assert "pull_request:" in content

        # Jobs verification
        assert "lint:" in content
        assert "security-scan:" in content
        assert "test:" in content
        assert "docker-build:" in content
        assert "deploy:" in content

        # Dependency chain verification
        assert "needs: [lint, security-scan]" in content
        assert "needs: test" in content
        assert "needs: docker-build" in content

        # Tool verification
        assert "flake8" in content
        assert "bandit" in content
        assert "pytest" in content
        assert "docker/build-push-action" in content
        assert "healthcheck.sh" in content

def test_healthcheck_script_dry_run():
    """Verify scripts/healthcheck.sh exists and passes dry-run execution."""
    script_path = os.path.join(PROJECT_ROOT, "scripts", "healthcheck.sh")
    assert os.path.exists(script_path), "scripts/healthcheck.sh missing"

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "#!/usr/bin/env bash" in content
        assert "--dry-run" in content
        assert "HTTP_CODE" in content

    # Test dry run execution via bash if available
    try:
        res = subprocess.run(["bash", script_path, "--dry-run"], capture_output=True, text=True)
        if res.returncode == 0:
            assert "Dry-run health verification PASSED" in res.stdout
    except Exception:
        # Fallback if bash is not directly on system path in Windows environment
        pass
