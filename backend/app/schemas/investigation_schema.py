from pydantic import BaseModel
from typing import List, Optional

class InvestigationItem(BaseModel):
    test: str
    rationale: str
    urgency: str

class InvestigationMap(BaseModel):
    first_line: List[InvestigationItem]
    second_line: List[InvestigationItem]
    scoring_systems: List[str]
    guideline: Optional[str] = None

class InvestigationRecommendation(BaseModel):
    condition: str
    investigations: InvestigationMap
