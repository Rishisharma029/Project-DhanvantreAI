from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DifferentialDiagnosisRequest(BaseModel):
    symptoms: List[str] = Field(..., example=["fever", "cough", "body pain", "fatigue"])
    onset_days: Optional[int] = Field(2, description="Duration of symptoms in days")
    severity_filter: Optional[str] = Field(None, description="Optional filter by minimum severity level")

class DifferentialCandidateDetail(BaseModel):
    rank: int
    condition_name: str
    icd11_code: str
    probability_percentage: str  # e.g., "91%"
    probability_score: float     # e.g., 0.91
    severity_level: str          # RED_EMERGENCY, HIGH_URGENT, MODERATE, LOW_MILD
    evidence: List[str]
    missing_findings: List[str]
    clinical_recommendation: str

class DifferentialDiagnosisResponse(BaseModel):
    reported_symptoms: List[str]
    total_candidates_evaluated: int
    differential_candidates: List[DifferentialCandidateDetail]
    execution_time_ms: int
