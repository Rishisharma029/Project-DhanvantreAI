import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.rag_schema import RAGQueryRequest, RAGPipelineResponse
from app.services.advanced_rag_engine import run_advanced_rag_pipeline

router = APIRouter(prefix="/rag", tags=["Advanced RAG Engine ⭐⭐⭐⭐⭐"])

@router.post("/query", response_model=RAGPipelineResponse)
def execute_rag_query(req: RAGQueryRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 6-Stage Advanced RAG Pipeline:
    Intent Detection -> Query Rewriting & Synonyms -> Hybrid Multi-Retrieval -> RRF Ranking -> Cross-Encoder Re-ranking (Top 10 Evidence) -> Context Compression & Synthesis.
    """
    try:
        return run_advanced_rag_pipeline(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Engine failure: {str(e)}")

@router.post("/explain-context")
def explain_rag_context(req: RAGQueryRequest, db: sqlite3.Connection = Depends(get_db)):
    """Inspect top 10 evidence chunks and compressed context payload for explainability."""
    res = run_advanced_rag_pipeline(req, db)
    return {
        "query": res.query,
        "intent": res.detected_intent,
        "top_10_evidence_chunks": res.top_10_evidence,
        "compressed_context": res.compressed_context,
        "latency_ms": res.latency_ms
    }
