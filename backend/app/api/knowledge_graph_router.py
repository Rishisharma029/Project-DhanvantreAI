import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.knowledge_graph_schema import KnowledgeGraphRequest, KnowledgeGraphResponse
from app.services.medical_knowledge_graph_engine import traverse_medical_knowledge_graph

router = APIRouter(prefix="/knowledge-graph", tags=["Medical Knowledge Graph ⭐⭐⭐⭐⭐"])

@router.post("/traverse", response_model=KnowledgeGraphResponse)
def traverse_knowledge_graph_endpoint(req: KnowledgeGraphRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 6-Tier Medical Knowledge Graph Traversal & Graph Reasoning:
    Medicine -> Ingredient -> Disease -> Symptoms -> Interactions -> Side Effects
    Enables multi-hop graph reasoning and clinical trajectory mapping.
    """
    try:
        return traverse_medical_knowledge_graph(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge Graph traversal failure: {str(e)}")

@router.get("/entity/{entity_name}", response_model=KnowledgeGraphResponse)
def get_entity_knowledge_graph(entity_name: str, db: sqlite3.Connection = Depends(get_db)):
    """Fetch Knowledge Graph node and edge network for a specific medical entity."""
    try:
        req = KnowledgeGraphRequest(query_entity=entity_name, max_depth=3)
        return traverse_medical_knowledge_graph(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge Graph lookup failure: {str(e)}")
