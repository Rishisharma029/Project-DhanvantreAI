from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, example="What are the side effects and interactions of Paracetamol for high fever?")
    max_chunks: int = Field(10, ge=1, le=20, description="Top N evidence chunks to retrieve")
    enable_compression: bool = Field(True, description="Enable context compression for LLM prompt")

class EvidenceChunkItem(BaseModel):
    chunk_id: str
    doc_type: str  # medicine, disease, symptom, interaction
    title: str
    content: str
    relevance_score: float
    rrf_score: float
    rank: int

class RAGPipelineResponse(BaseModel):
    query: str
    detected_intent: str
    rewritten_queries: List[str]
    synonyms_expanded: List[str]
    top_10_evidence: List[EvidenceChunkItem]
    compressed_context: str
    synthesized_answer: str
    latency_ms: int
