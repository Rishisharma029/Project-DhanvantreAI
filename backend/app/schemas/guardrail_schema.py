from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GuardrailViolationItem(BaseModel):
    check_name: str # Medicine Names, Dosages, Warnings, Contraindications, Safety Instructions
    severity: str # Critical, High, Moderate
    message: str
    failed_target: Optional[str] = None

class GuardrailVerifyRequest(BaseModel):
    medicine_name: Optional[str] = Field(None, description="Medicine or active ingredient name")
    dosage_text: Optional[str] = Field(None, description="Proposed dosage e.g. '4000mg per 24 hours'")
    patient_age: Optional[int] = 30
    patient_allergies: Optional[List[str]] = []
    is_pregnant: Optional[bool] = False
    has_kidney_disease: Optional[bool] = False
    has_liver_disease: Optional[bool] = False
    active_medications: Optional[List[str]] = []
    has_disclaimer: Optional[bool] = True
    generated_text: Optional[str] = ""

class GuardrailVerifyResponse(BaseModel):
    is_valid: bool
    status: str # PASSED, REGENERATE_REQUIRED
    total_violations: int
    violations: List[GuardrailViolationItem]
    corrective_feedback_prompt: Optional[str] = None
