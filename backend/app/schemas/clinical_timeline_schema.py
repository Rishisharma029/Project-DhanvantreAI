from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum

class TimelineStage(str, Enum):
    SYMPTOMS = "SYMPTOMS"
    ASSESSMENT = "ASSESSMENT"
    MEDICINES = "MEDICINES"
    FOLLOWUP = "FOLLOWUP"
    RECOVERY = "RECOVERY"

class NodeStatus(str, Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    SCHEDULED = "SCHEDULED"
    RECOMMENDED = "RECOMMENDED"

class TimelineNode(BaseModel):
    stage: TimelineStage
    title: str
    description: str
    timeline_day: str  # e.g., "Day 1-2"
    status: NodeStatus
    clinical_notes: List[str] = Field(default_factory=list)
    key_metrics: Dict[str, str] = Field(default_factory=dict)
    evidence_sources: List[str] = Field(default_factory=list)

class ClinicalTimelineRequest(BaseModel):
    reported_symptoms: List[str] = Field(..., json_schema_extra={"example": ["fever", "cough", "fatigue"]})
    diagnosis_name: Optional[str] = Field(default=None, json_schema_extra={"example": ["Acute Bronchitis"]})
    prescribed_medicines: Optional[List[str]] = Field(default=[], json_schema_extra={"example": ["Amoxicillin", "Paracetamol"]})
    onset_days_ago: Optional[int] = Field(default=2, ge=0, le=30)
    patient_age: Optional[int] = Field(default=35, ge=0, le=120)

class ClinicalTimelineResponse(BaseModel):
    timeline_id: str
    condition_name: str
    total_estimated_days: int
    current_stage: TimelineStage
    timeline_nodes: List[TimelineNode]
    key_milestones: List[str]
    red_flag_warnings: List[str]
