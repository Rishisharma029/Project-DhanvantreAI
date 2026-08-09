from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AlternativeDiseaseExplain(BaseModel):
    disease_name: str
    confidence: float
    confidence_percentage: str
    matching_symptoms: List[str]
    differentiation_reason: str

class ExplainabilityRequest(BaseModel):
    disease_name: str = Field(..., min_length=1, description="Primary predicted disease name e.g. 'Dengue'")
    medicine_name: Optional[str] = Field(None, description="Recommended medicine e.g. 'Paracetamol 650mg'")
    reported_symptoms: List[str] = Field(..., min_length=1, description="Symptoms reported by user")
    confidence_score: Optional[float] = 0.85

class ExplainabilityResponse(BaseModel):
    primary_disease: str
    why_disease: str
    why_medicine: str
    why_confidence: Dict[str, Any]
    alternative_diseases: List[AlternativeDiseaseExplain]
    missing_symptoms: List[str]
    disclaimer: str = "Reference information only, not personalized prescribing. Consult a licensed physician or pharmacist for medical advice."
