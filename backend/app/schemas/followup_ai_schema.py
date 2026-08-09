from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class SymptomProgressionStatus(str, Enum):
    IMPROVING = "IMPROVING"
    STABLE = "STABLE"
    WORSENING = "WORSENING"
    RESOLVED = "RESOLVED"

class FollowUpAssessmentRequest(BaseModel):
    session_id: str = Field(..., json_schema_extra={"example": "SESS-88120"})
    feeling_better: bool = Field(..., json_schema_extra={"example": True})
    new_symptoms: Optional[List[str]] = Field(default_factory=list, json_schema_extra={"example": ["mild dizziness"]})
    resolved_symptoms: Optional[List[str]] = Field(default_factory=list, json_schema_extra={"example": ["fever", "body pain"]})
    current_medication_adherence: Optional[bool] = Field(default=True)

class FollowUpAssessmentResponse(BaseModel):
    followup_id: str
    progression_status: SymptomProgressionStatus
    updated_risk_level: str  # LOW_GREEN, MODERATE_YELLOW, HIGH_ORANGE, CRITICAL_RED
    clinical_assessment_update: str
    recommended_actions: List[str]
    next_followup_days: int
