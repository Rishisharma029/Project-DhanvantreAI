from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class FeedbackType(str, Enum):
    RATING = "RATING"
    INCORRECT_SUGGESTION = "INCORRECT_SUGGESTION"
    MISSING_DATA = "MISSING_DATA"
    PROMPT_OPTIMIZATION = "PROMPT_OPTIMIZATION"

class ReportedCategory(str, Enum):
    MISDIAGNOSIS = "MISDIAGNOSIS"
    WRONG_DOSAGE = "WRONG_DOSAGE"
    MISSING_DRUG = "MISSING_DRUG"
    MISSING_SYMPTOM = "MISSING_SYMPTOM"
    RAG_HALLUCINATION = "RAG_HALLUCINATION"
    OTHER = "OTHER"

class FeedbackSubmissionRequest(BaseModel):
    user_id: Optional[int] = Field(default=None)
    feedback_type: FeedbackType = Field(..., json_schema_extra={"example": "INCORRECT_SUGGESTION"})
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    query_or_context: str = Field(..., json_schema_extra={"example": "Dosage of Paracetamol for 5-year-old child with high fever"})
    ai_response: str = Field(..., json_schema_extra={"example": "Take 1000mg Paracetamol every 4 hours."})
    user_comment: Optional[str] = Field(default=None, json_schema_extra={"example": "1000mg is adult dosage, too high for a 5-year-old."})
    reported_category: Optional[ReportedCategory] = Field(default=ReportedCategory.WRONG_DOSAGE)
    suggested_correction: Optional[str] = Field(default=None, json_schema_extra={"example": "Pediatric Paracetamol is 10-15mg/kg per dose."})

class FeedbackSubmissionResponse(BaseModel):
    feedback_id: str
    status: str
    message: str
    continuous_improvement_action: str

class FeedbackAnalyticsSummary(BaseModel):
    total_feedback_count: int
    average_rating: float
    total_incorrect_reports: int
    total_missing_data_reports: int
    prompt_optimization_triggers: int
    top_reported_categories: Dict[str, int]
    improvement_actions_log: List[str]
