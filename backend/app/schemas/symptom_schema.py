from pydantic import BaseModel, Field
from typing import Optional, List

class SymptomProcessRequest(BaseModel):
    text: str = Field(..., min_length=2, description="Natural language text containing patient symptoms")

class ExtractedSymptomItem(BaseModel):
    raw_term: str
    canonical_name: str
    severity: str = "Moderate" # Mild, Moderate, Severe, Emergency
    severity_weight: int = 1

class CandidateDiseaseMatch(BaseModel):
    disease_name: str
    matched_symptoms_count: int
    total_disease_symptoms: int
    match_percentage: float
    severity_level: str = "Moderate"
    description: Optional[str] = ""

class SymptomProcessResponse(BaseModel):
    input_text: str
    extracted_symptoms: List[ExtractedSymptomItem]
    canonical_symptom_names: List[str]
    overall_severity: str = "Moderate" # Mild, Moderate, Severe, Emergency
    candidate_diseases: List[CandidateDiseaseMatch]

class SymptomSearchResponse(BaseModel):
    id: int
    name: str
    severity_weight: int
