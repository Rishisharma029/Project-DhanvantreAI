import sqlite3
from fastapi import APIRouter, Depends, Path
from app.database import get_db
from app.schemas.cache_schema import CacheStatsResponse, CacheClearResponse, CacheWarmupResponse
from app.services.cache_layer_service import cache_engine

router = APIRouter(prefix="/cache", tags=["Cache Layer"])

@router.get("/stats", response_model=CacheStatsResponse)
def get_cache_stats_endpoint():
    """Retrieve Cache hit/miss stats, active namespaces, and key counts."""
    return cache_engine.get_stats()

@router.delete("/clear/{namespace}", response_model=CacheClearResponse)
def clear_cache_namespace_endpoint(namespace: str = Path(..., description="search, medicine, disease, aicontext, session, or all")):
    """Clear cached entries in specified namespace or 'all'."""
    deleted_cnt = cache_engine.clear_namespace(namespace)
    return CacheClearResponse(
        namespace_cleared=namespace,
        keys_deleted=deleted_cnt,
        message=f"Cleared {deleted_cnt} cached entries in '{namespace}' namespace."
    )

@router.post("/warmup", response_model=CacheWarmupResponse)
def warmup_cache_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """Pre-warm medicine, disease, and AI context cache keys."""
    return cache_engine.warmup_cache(db)
