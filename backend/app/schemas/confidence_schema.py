from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ConfidenceSignalBreakdown(BaseModel):
    disease_model_score: float
    disease_model_weighted: float # Score * 0.40
    symptom_coverage_ratio: float
    symptom_coverage_weighted: float # Ratio * 0.40
    interaction_penalty: float # 0.0 to -0.30
    contradiction_penalty: float # 0.0 to -0.50
    high_alignment_bonus: float # 0.0 or +0.10

class ConfidenceCalibrateRequest(BaseModel):
    disease_name: str = Field(..., min_length=1, description="Predicted disease name")
    base_disease_confidence: float = Field(..., ge=0.0, le=1.0, description="Base probability score from disease model (0.0 to 1.0)")
    matched_symptoms_count: int = Field(..., ge=0, description="Number of matched symptoms")
    total_disease_symptoms_count: int = Field(..., ge=1, description="Total hallmark symptoms required for disease")
    interaction_severity: Optional[str] = "None" # Major, Moderate, Minor, None
    safety_grade: Optional[str] = "SAFE" # SAFE, CAUTION, UNSAFE, CONTRAINDICATED
    safety_score: Optional[float] = 100.0 # 0.0 to 100.0

class ConfidenceCalibrateResponse(BaseModel):
    disease_name: str
    final_confidence_score: float # 0.0 to 1.0
    final_confidence_percentage: str # e.g. "85%"
    confidence_grade: str # High Confidence, Moderate Confidence, Low Confidence
    signal_breakdown: ConfidenceSignalBreakdown
    disclaimer: str = "Reference information only, not personalized prescribing. Consult a licensed physician or pharmacist for medical advice."
