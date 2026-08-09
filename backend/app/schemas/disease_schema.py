from pydantic import BaseModel, Field
from typing import Optional, List

class DiseasePredictRequest(BaseModel):
    symptoms: List[str] = Field(..., min_length=1, description="List of reported symptom names e.g. ['fever', 'headache']")
    top_n: Optional[int] = 5

class PredictedDiseaseItem(BaseModel):
    disease_name: str
    confidence: float # 0.0 to 1.0
    confidence_percentage: float # 0.0 to 100.0
    severity: str # Emergency, Severe, Moderate, Mild
    matching_symptoms: List[str]
    missing_symptoms: List[str]
    description: Optional[str] = ""
    precautions: Optional[List[str]] = []

class DiseasePredictResponse(BaseModel):
    input_symptoms: List[str]
    total_matches_found: int
    top_diseases: List[PredictedDiseaseItem]
