from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class CacheStatsResponse(BaseModel):
    backend_mode: str # Redis or In-Memory Hybrid Fallback
    total_keys: int
    keys_by_namespace: Dict[str, int]
    hits: int
    misses: int
    hit_ratio_percentage: str
    status: str

class CacheClearResponse(BaseModel):
    namespace_cleared: str
    keys_deleted: int
    message: str

class CacheWarmupResponse(BaseModel):
    total_keys_warmed: int
    namespaces_warmed: List[str]
    duration_ms: float
    status: str
