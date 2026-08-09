import os
import sys
import time
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.services.cache_layer_service import cache_engine

client = TestClient(app)

def test_cache_namespaces_set_get():
    # 1. Search namespace
    cache_engine.set("search", "paracetamol", {"results": 12}, 60)
    assert cache_engine.get("search", "paracetamol") == {"results": 12}

    # 2. Medicine namespace
    cache_engine.set("medicine", "101", {"name": "Crocin 650"}, 60)
    assert cache_engine.get("medicine", "101")["name"] == "Crocin 650"

    # 3. Disease namespace
    cache_engine.set("disease", "202", {"name": "Dengue Fever"}, 60)
    assert cache_engine.get("disease", "202")["name"] == "Dengue Fever"

    # 4. AI Context namespace
    cache_engine.set("aicontext", "sess-1", {"prompt_tokens": 150}, 60)
    assert cache_engine.get("aicontext", "sess-1")["prompt_tokens"] == 150

    # 5. Session namespace
    cache_engine.set("session", "user-1", {"role": "admin"}, 60)
    assert cache_engine.get("session", "user-1")["role"] == "admin"

def test_cache_ttl_expiration():
    cache_engine.set("search", "short_key", {"data": 123}, ttl_sec=1)
    assert cache_engine.get("search", "short_key") == {"data": 123}
    time.sleep(1.1)
    assert cache_engine.get("search", "short_key") is None

def test_cache_stats_endpoint():
    res = client.get("/api/v1/cache/stats")
    assert res.status_code == 200
    data = res.json()
    assert "hits" in data
    assert "keys_by_namespace" in data

def test_cache_clear_endpoint():
    cache_engine.set("medicine", "temp_med", "data", 60)
    res = client.delete("/api/v1/cache/clear/medicine")
    assert res.status_code == 200
    assert res.json()["keys_deleted"] >= 1
    assert cache_engine.get("medicine", "temp_med") is None

def test_cache_warmup_endpoint():
    res = client.post("/api/v1/cache/warmup")
    assert res.status_code == 200
    data = res.json()
    assert data["total_keys_warmed"] >= 1
    assert data["status"] == "SUCCESS"
