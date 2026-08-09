from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class ImageType(str, Enum):
    SKIN_RASH = "SKIN_RASH"
    MEDICATION_LABEL = "MEDICATION_LABEL"
    PILL_IDENTIFICATION = "PILL_IDENTIFICATION"
    WOUND_PROGRESSION = "WOUND_PROGRESSION"

class ImageAIRequest(BaseModel):
    image_type: ImageType = Field(..., json_schema_extra={"example": "SKIN_RASH"})
    image_base64_or_path: str = Field(..., json_schema_extra={"example": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."})
    clinical_context: Optional[str] = Field(default="Mildly itchy erythematous rash on forearm for 3 days.")

class ImageAIResponse(BaseModel):
    analysis_id: str
    image_type: ImageType
    detected_features: List[str]
    preliminary_assessment: str
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    disclaimer: str
    recommended_next_steps: List[str]
