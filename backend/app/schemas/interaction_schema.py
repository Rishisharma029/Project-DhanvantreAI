from pydantic import BaseModel, Field
from typing import Optional, List

class PairwiseCheckRequest(BaseModel):
    drug_a: str = Field(..., min_length=1, description="First drug name or ingredient e.g. 'Aspirin'")
    drug_b: str = Field(..., min_length=1, description="Second drug name or ingredient e.g. 'Warfarin'")

class RegimenCheckRequest(BaseModel):
    medicines: List[str] = Field(..., min_length=2, description="List of medicines/drugs in regimen")

class CurrentVsRecommendedRequest(BaseModel):
    current_medicines: List[str] = Field(..., description="List of patient's current active medicines")
    recommended_medicines: List[str] = Field(..., min_length=1, description="List of proposed/recommended medicines")

class DrugInteractionItem(BaseModel):
    drug_a: str
    drug_b: str
    severity: str # Major, Moderate, Minor, Safe
    severity_icon: str # 🔴 Major, 🟡 Moderate, 🟢 Minor
    description: str
    risk_level: int # 3 = Major, 2 = Moderate, 1 = Minor, 0 = Safe

class InteractionCheckResponse(BaseModel):
    has_interactions: bool
    highest_severity: str # Major, Moderate, Minor, Safe
    total_interactions_found: int
    interactions: List[DrugInteractionItem]

class CurrentVsRecommendedResponse(BaseModel):
    has_conflicts: bool
    highest_severity: str
    total_conflicts_found: int
    conflicts: List[DrugInteractionItem]
