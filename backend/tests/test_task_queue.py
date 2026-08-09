import os
import sys
import time
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def wait_for_task_completion(task_id: str, timeout_sec: float = 3.0):
    start = time.time()
    while time.time() - start < timeout_sec:
        res = client.get(f"/api/v1/tasks/status/{task_id}")
        data = res.json()
        if data["status"] in ["COMPLETED", "FAILED", "CANCELLED"]:
            return data
        time.sleep(0.05)
    return client.get(f"/api/v1/tasks/status/{task_id}").json()

def test_enqueue_pdf_generation():
    payload = {"task_type": "pdf_generation", "payload": {"title": "Test Lab Report", "document_type": "Blood Test"}}
    res = client.post("/api/v1/tasks/enqueue", json=payload)
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    data = wait_for_task_completion(task_id)
    assert data["status"] == "COMPLETED"
    assert "document_name" in data["result"]

def test_enqueue_email_sending():
    payload = {"task_type": "email_sending", "payload": {"recipient_email": "patient@hospital.org", "subject": "Test Alert"}}
    res = client.post("/api/v1/tasks/enqueue", json=payload)
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    data = wait_for_task_completion(task_id)
    assert data["status"] == "COMPLETED"

def test_enqueue_database_sync():
    payload = {"task_type": "database_sync", "payload": {}}
    res = client.post("/api/v1/tasks/enqueue", json=payload)
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    data = wait_for_task_completion(task_id)
    assert data["status"] == "COMPLETED"

def test_enqueue_cache_refresh():
    payload = {"task_type": "cache_refresh", "payload": {"namespace": "diseases_cache"}}
    res = client.post("/api/v1/tasks/enqueue", json=payload)
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    data = wait_for_task_completion(task_id)
    assert data["status"] == "COMPLETED"

def test_enqueue_ai_preprocessing():
    payload = {"task_type": "ai_preprocessing", "payload": {"query_text": "severe headache and nausea"}}
    res = client.post("/api/v1/tasks/enqueue", json=payload)
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    data = wait_for_task_completion(task_id)
    assert data["status"] == "COMPLETED"

def test_invalid_task_type():
    res = client.post("/api/v1/tasks/enqueue", json={"task_type": "invalid_worker"})
    assert res.status_code == 400

def test_cancel_task():
    payload = {"task_type": "pdf_generation", "payload": {}}
    res = client.post("/api/v1/tasks/enqueue", json=payload)
    task_id = res.json()["task_id"]

    cancel_res = client.post(f"/api/v1/tasks/cancel/{task_id}")
    assert cancel_res.status_code in [200, 400]
