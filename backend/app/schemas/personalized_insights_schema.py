from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class InsightCategory(str, Enum):
    MEDICINE_ADHERENCE = "MEDICINE_ADHERENCE"
    WATER_HYDRATION = "WATER_HYDRATION"
    LIFESTYLE_SUGGESTION = "LIFESTYLE_SUGGESTION"
    HEALTH_EDUCATION = "HEALTH_EDUCATION"

class InsightPriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    DAILY_ROUTINE = "DAILY_ROUTINE"

class HealthInsightItem(BaseModel):
    insight_id: str
    category: InsightCategory
    title: str
    description: str
    action_prompt: str
    priority: InsightPriority
    timestamp: str

class PersonalizedInsightsRequest(BaseModel):
    user_id: Optional[int] = Field(default=None)
    patient_age: Optional[int] = Field(default=30, ge=0, le=120)
    current_medications: Optional[List[str]] = Field(default_factory=list, json_schema_extra={"example": ["Paracetamol", "Amlodipine"]})
    chronic_conditions: Optional[List[str]] = Field(default_factory=list, json_schema_extra={"example": ["Hypertension"]})

class PersonalizedInsightsResponse(BaseModel):
    user_id: Optional[int]
    date: str
    total_insights: int
    insights: List[HealthInsightItem]
