from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum

class QualityGrade(str, Enum):
    EXCELLENT = "EXCELLENT"      # 90 - 100
    GOOD = "GOOD"                # 75 - 89
    ACCEPTABLE = "ACCEPTABLE"    # 60 - 74
    POOR = "POOR"                # 40 - 59
    UNSAFE = "UNSAFE"            # < 40

class MetricScore(BaseModel):
    metric_name: str
    score: float = Field(..., ge=0.0, le=100.0)
    status: str  # PASS, WARNING, FAIL
    explanation: str

class QualityEvaluationRequest(BaseModel):
    query: str = Field(..., json_schema_extra={"example": "What is the recommended treatment and dosage for Paracetamol in acute fever?"})
    ai_response_text: str = Field(..., json_schema_extra={"example": "Paracetamol 500mg every 6 hours is indicated for acute fever. [WHO Guidelines Sec 4.2]"})
    retrieved_context_chunks: List[str] = Field(..., json_schema_extra={"example": ["Paracetamol 500mg every 4-6 hours for fever relief. Maximum daily dose 4000mg."]})
    citations: Optional[List[str]] = Field(default=["WHO Guidelines Sec 4.2"])

class QualityEvaluationResponse(BaseModel):
    evaluation_id: str
    overall_quality_score: float = Field(..., ge=0.0, le=100.0)
    quality_grade: QualityGrade
    is_approved_for_delivery: bool
    metrics: Dict[str, MetricScore]
    detailed_diagnostics: List[str]
    recommended_remediations: List[str]
