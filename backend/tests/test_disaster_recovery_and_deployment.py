import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.services.disaster_recovery_service import disaster_recovery_engine

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
client = TestClient(app)

def test_encrypted_backup_creation_and_restore_verification():
    """Verify AES-256 encrypted database backup creation and test restore verification."""
    # 1. Trigger Encrypted Backup
    backup_res = disaster_recovery_engine.create_encrypted_backup()
    assert backup_res["status"] == "success"
    assert backup_res["backup_filename"].endswith(".enc.db")
    assert os.path.exists(backup_res["backup_path"])

    # 2. Verify Restore Integrity
    restore_res = disaster_recovery_engine.restore_and_verify_backup(backup_res["backup_path"])
    assert restore_res["is_valid"] is True
    assert restore_res["integrity_check"] == "ok"
    assert restore_res["table_count"] > 0

    # Clean up test backup file
    if os.path.exists(backup_res["backup_path"]):
        os.remove(backup_res["backup_path"])

def test_list_backups():
    """Verify listing encrypted database backups."""
    backups = disaster_recovery_engine.list_backups()
    assert isinstance(backups, list)

def test_multi_cloud_deployment_manifests_exist():
    """Verify deployment manifests exist for Railway, Render, AWS, GCP, and Azure."""
    # 1. Railway
    railway_path = os.path.join(PROJECT_ROOT, "railway.json")
    assert os.path.exists(railway_path)

    # 2. Render
    render_path = os.path.join(PROJECT_ROOT, "render.yaml")
    assert os.path.exists(render_path)

    # 3. AWS
    aws_apprunner = os.path.join(PROJECT_ROOT, "deployment", "aws", "AppRunner.yaml")
    aws_ecs = os.path.join(PROJECT_ROOT, "deployment", "aws", "ecs-task-definition.json")
    assert os.path.exists(aws_apprunner)
    assert os.path.exists(aws_ecs)

    # 4. GCP
    gcp_cloudrun = os.path.join(PROJECT_ROOT, "deployment", "gcp", "cloudrun-service.yaml")
    gcp_appengine = os.path.join(PROJECT_ROOT, "deployment", "gcp", "app.yaml")
    assert os.path.exists(gcp_cloudrun)
    assert os.path.exists(gcp_appengine)

    # 5. Azure
    azure_bicep = os.path.join(PROJECT_ROOT, "deployment", "azure", "azure-container-app.bicep")
    assert os.path.exists(azure_bicep)
