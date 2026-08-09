from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class EvidenceCitationRequest(BaseModel):
    medical_query: str = Field(..., example="What are the clinical guidelines and drug interactions for Paracetamol with Warfarin?")
    proposed_explanation: Optional[str] = Field(None, description="Optional explanation to evaluate for evidence citations")
    enforce_strict_grounding: bool = Field(True, description="Strictly flag or reject statements lacking evidence citations")

class CitationSourceItem(BaseModel):
    source_tier: str            # DRUG_DATABASE, CLINICAL_GUIDELINE, DRUG_INTERACTION, MEDICAL_LITERATURE
    source_title: str
    reference_code_id: str      # e.g., RX-MED-99, WHO-TRS-961, INTER-WARN-12, PMID-34981204
    snippet: str
    confidence_weight: float

class CitedStatementItem(BaseModel):
    statement: str
    is_supported: bool
    primary_citation: Optional[CitationSourceItem] = None
    secondary_citations: List[CitationSourceItem] = []

class EvidenceCitationResponse(BaseModel):
    query: str
    groundness_score: float     # 0.0 to 1.0 (Percentage of supported statements)
    contains_unsupported_statements: bool
    cited_statements: List[CitedStatementItem]
    evidence_sources_summary: Dict[str, int]
    execution_time_ms: int
