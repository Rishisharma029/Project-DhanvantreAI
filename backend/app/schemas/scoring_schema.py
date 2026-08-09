from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ScoringResult(BaseModel):
    score: float
    max_score: float
    risk_category: str
    clinical_action: str
    explanation: str
    score_name: str
