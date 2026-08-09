from pydantic import BaseModel, Field
from typing import Optional, List

class DietItem(BaseModel):
    disease_name: str
    diet_recommendation: str

class PrecautionItem(BaseModel):
    disease_name: str
    precaution: str

class WorkoutItem(BaseModel):
    disease_name: str
    workout_recommendation: str

class SideEffectInfo(BaseModel):
    medicine_name: str
    side_effect_name: str
    frequency: str = "Common"

class InteractionInfo(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    severity_icon: str
    description: str

class Disease360KnowledgeResponse(BaseModel):
    disease_id: int
    disease_name: str
    severity_level: str
    description: str
    symptoms: List[str] = []
    diets: List[str] = []
    precautions: List[str] = []
    workouts: List[str] = []

class Medicine360KnowledgeResponse(BaseModel):
    medicine_id: int
    canonical_name: str
    brand_name: str
    generic_name: Optional[str] = None
    composition: Optional[str] = None
    price_inr: Optional[float] = None
    manufacturer_name: Optional[str] = None
    ingredients: List[str] = []
    side_effects: List[SideEffectInfo] = []
    interactions: List[InteractionInfo] = []
    uses: List[str] = []
    substitutes: List[str] = []
