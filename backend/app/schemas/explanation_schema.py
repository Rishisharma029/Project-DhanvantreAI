from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExplanationRequest(BaseModel):
    disease_or_medicine_name: str = Field(..., example="Paracetamol")
    reported_symptoms: Optional[List[str]] = Field(default=[], example=["fever", "headache"])
    mode: str = Field("BOTH", description="PATIENT, PROFESSIONAL, or BOTH")

class PatientModeExplanation(BaseModel):
    summary: str
    simple_explanation: str
    lifestyle_care_steps: List[str]
    red_flag_warnings: List[str]

class ProfessionalModeExplanation(BaseModel):
    clinical_summary: str
    icd11_code: str
    mechanism_of_action: str
    pharmacological_pathway: str
    evidence_citations: List[str]
    contraindications: List[str]
    black_box_warnings: Optional[str] = None

class DualExplanationResponse(BaseModel):
    target_name: str
    mode_requested: str
    patient_explanation: Optional[PatientModeExplanation] = None
    professional_explanation: Optional[ProfessionalModeExplanation] = None
    execution_time_ms: int
