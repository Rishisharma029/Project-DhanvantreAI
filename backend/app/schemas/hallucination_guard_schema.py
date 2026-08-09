from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class ClaimVerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTED = "CONTRADICTED"

class ExtractedClaim(BaseModel):
    claim_id: str
    claim_text: str
    category: str  # DOSAGE, CONTRAINDICATION, DIAGNOSIS, SIDE_EFFECT, GENERAL_MEDICAL
    status: ClaimVerificationStatus
    grounding_source: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    verification_reason: str

class HallucinationGuardRequest(BaseModel):
    llm_response_text: str = Field(..., json_schema_extra={"example": "Paracetamol 500mg treats high fever. Amoxicillin cures viral flu instantly."})
    context_evidence_chunks: List[str] = Field(..., json_schema_extra={"example": ["Paracetamol is an antipyretic for fever relief.", "Amoxicillin is an antibiotic for bacterial infections, ineffective against viral flu."]})
    allow_auto_regeneration: bool = Field(default=True)

class HallucinationGuardResponse(BaseModel):
    is_safe: bool
    hallucination_detected: bool
    total_claims_extracted: int
    supported_claims_count: int
    unsupported_claims_count: int
    grounding_score: float = Field(..., ge=0.0, le=100.0)
    action_taken: str  # PASSED, REGENERATED_AND_SANITIZED, REJECTED
    verified_response_text: str
    claims: List[ExtractedClaim]
