from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class DashboardStep(str, Enum):
    SYMPTOMS = "SYMPTOMS"
    DISEASE = "DISEASE"
    CONFIDENCE = "CONFIDENCE"
    EVIDENCE = "EVIDENCE"
    MEDICINES = "MEDICINES"
    SAFETY = "SAFETY"
    FINAL_EXPLANATION = "FINAL_EXPLANATION"

class DashboardStepDetail(BaseModel):
    step_number: int = Field(..., ge=1, le=7)
    step_name: DashboardStep
    title: str
    summary: str
    data_payload: Dict[str, Any] = Field(default_factory=dict)
    is_verified: bool = Field(default=True)

class ExplainabilityDashboardRequest(BaseModel):
    reported_symptoms: List[str] = Field(..., json_schema_extra={"example": ["fever", "cough", "fatigue"]})
    suspected_disease: Optional[str] = Field(default="Acute Bronchitis")
    prescribed_medicines: Optional[List[str]] = Field(default=["Amoxicillin", "Paracetamol"])
    patient_age: Optional[int] = Field(default=35, ge=0, le=120)
    is_pregnant: Optional[bool] = Field(default=False)

class ExplainabilityDashboardResponse(BaseModel):
    dashboard_id: str
    transparency_score: float = Field(..., ge=0.0, le=100.0)
    steps: List[DashboardStepDetail]
    clinical_summary: str
