from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class HybridSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query e.g. 'antifungal medication for skin rash'")
    top_k: Optional[int] = 5
    fts_weight: Optional[float] = 0.5
    vector_weight: Optional[float] = 0.5
    rrf_k: Optional[int] = 60

class MedicalDocumentItem(BaseModel):
    document_id: str
    doc_type: str # medicine, disease, symptom, interaction
    title: str
    content_snippet: str
    rrf_score: float # Unified RRF score
    fts_rank: Optional[int] = None
    vector_rank: Optional[int] = None
    bm25_score: Optional[float] = None
    semantic_similarity: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = {}

class HybridSearchResponse(BaseModel):
    query: str
    total_results: int
    execution_time_ms: float
    documents: List[MedicalDocumentItem]
