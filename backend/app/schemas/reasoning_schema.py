from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PhysicianReasoningRequest(BaseModel):
    reported_symptoms: List[str] = Field(..., example=["chest pain", "shortness of breath", "sweating"])
    onset_days: Optional[int] = Field(1, description="Onset duration in days")
    severity_scale: Optional[str] = Field("Moderate", description="Mild, Moderate, Severe")
    patient_age: Optional[int] = Field(45, description="Patient age in years")
    chronic_conditions: Optional[List[str]] = Field(default=[], example=["Hypertension"])

class DifferentialCandidateItem(BaseModel):
    disease_name: str
    icd11_code: str
    status: str  # RULED_IN or RULED_OUT
    probability_score: float
    match_rationale: str
    rejection_rationale: Optional[str] = None
    matched_symptoms: List[str]
    missing_symptoms: List[str]

class PhysicianReasoningResponse(BaseModel):
    primary_diagnosis: str
    icd11_code: str
    overall_confidence: float
    evidence_summary: str
    rule_in_rationale: str
    supporting_evidence: List[str]
    differential_matrix: List[DifferentialCandidateItem]
    missing_pathognomonic_symptoms: List[str]
    recommended_clinical_next_steps: List[str]
    execution_time_ms: int
