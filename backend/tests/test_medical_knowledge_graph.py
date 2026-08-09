import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db
from app.services.medical_knowledge_graph_engine import traverse_medical_knowledge_graph
from app.schemas.knowledge_graph_schema import KnowledgeGraphRequest, GraphNodeType

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_6_tier_graph_traversal():
    """Verify 6-tier knowledge graph traversal (Medicine -> Ingredient -> Disease -> Symptoms -> Interactions -> Side Effects)."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = KnowledgeGraphRequest(query_entity="Paracetamol", max_depth=3)
    res = traverse_medical_knowledge_graph(req, conn)
    conn.close()

    assert "Paracetamol" in res.entity_name

    assert res.total_nodes >= 6
    assert res.total_edges >= 5

    node_types = {n.node_type for n in res.nodes}
    expected_types = {
        GraphNodeType.MEDICINE,
        GraphNodeType.INGREDIENT,
        GraphNodeType.DISEASE,
        GraphNodeType.SYMPTOM,
        GraphNodeType.INTERACTION,
        GraphNodeType.SIDE_EFFECT
    }
    assert expected_types.issubset(node_types)
    assert len(res.graph_reasoning_paths) >= 2

def test_knowledge_graph_api_endpoints():
    """Test HTTP REST endpoints for Knowledge Graph."""
    # 1. POST Traverse
    payload = {"query_entity": "Amoxicillin", "max_depth": 3}
    post_res = client.post(f"{settings.API_V1_STR}/knowledge-graph/traverse", json=payload)
    assert post_res.status_code == 200
    data = post_res.json()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) >= 6

    # 2. GET Entity Lookup
    get_res = client.get(f"{settings.API_V1_STR}/knowledge-graph/entity/Pneumonia")
    assert get_res.status_code == 200
    g_data = get_res.json()
    assert "graph_reasoning_paths" in g_data
