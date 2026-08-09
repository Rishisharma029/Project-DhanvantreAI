from pydantic import BaseModel, Field
from typing import Optional, List

class RecommendationRequest(BaseModel):
    disease: str = Field(..., min_length=2, description="Target disease or condition e.g. 'Fungal infection'")
    max_recommendations: Optional[int] = 5

class AlternativeMedicine(BaseModel):
    substitute_name: str
    price_inr: Optional[float] = None
    manufacturer: Optional[str] = ""

class SingleRecommendationItem(BaseModel):
    medicine: str
    reason: str
    confidence: str # e.g. "95%"
    confidence_score: float # 0.95
    price_inr: Optional[float] = None
    manufacturer: Optional[str] = ""
    composition: Optional[str] = ""
    alternatives: List[AlternativeMedicine] = []

class RecommendationResponse(BaseModel):
    disease: str
    recommendation_count: int
    recommendations: List[SingleRecommendationItem]
