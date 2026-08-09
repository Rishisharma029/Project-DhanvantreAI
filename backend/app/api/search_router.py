import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.search_schema import (
    HybridSearchRequest, HybridSearchResponse
)
from app.services.hybrid_search_engine import execute_hybrid_search

router = APIRouter(prefix="/search", tags=["Hybrid Search Engine ⭐⭐⭐⭐⭐"])

@router.post("/hybrid", response_model=HybridSearchResponse)
def hybrid_search_endpoint(body: HybridSearchRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute Hybrid Search:
    Combines PostgreSQL/SQLite Full-Text Search (FTS), BM25 Lexical Ranking, Semantic Vector Similarity, and Reciprocal Rank Fusion (RRF).
    Returns top relevant medical documents with rank score breakdowns.
    """
    return execute_hybrid_search(body, db)
