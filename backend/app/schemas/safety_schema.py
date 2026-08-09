from pydantic import BaseModel, Field
from typing import Optional, List

class PatientProfileInput(BaseModel):
    age: Optional[int] = 30
    gender: Optional[str] = "Male"
    pregnancy_status: Optional[bool] = False
    allergies: Optional[List[str]] = []
    chronic_diseases: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []

class SafetyValidateRequest(BaseModel):
    medicine_name: str = Field(..., min_length=1, description="Medicine or active ingredient name e.g. 'Augmentin 625 Duo'")
    medicine_id: Optional[int] = None
    patient_profile: PatientProfileInput

class SafetyWarningItem(BaseModel):
    check_type: str # Allergies, Pregnancy, Age, Kidney Disease, Liver Disease, Pediatric, Geriatric, Contraindications, Drug Interactions
    severity: str # Severe, Moderate, Info
    severity_icon: str # 🔴 Severe, 🟡 Moderate, ℹ️ Info
    message: str
    impact_score: float # Deduction from 100

class SafetyValidateResponse(BaseModel):
    medicine_name: str
    safety_score: float # 0.0 to 100.0
    safety_score_percentage: str # e.g. "95%"
    safety_grade: str # SAFE, CAUTION, UNSAFE, CONTRAINDICATED
    is_safe_to_take: bool
    total_warnings: int
    warnings: List[SafetyWarningItem]
