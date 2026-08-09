from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GuidelineMatchRequest(BaseModel):
    condition_name: str = Field(..., example="Pneumonia")
    reported_symptoms: Optional[List[str]] = Field(default=[], example=["cough", "fever", "chest pain"])
    authority_filter: Optional[str] = Field(None, description="Optional filter by authority: WHO, CDC, NICE, NATIONAL_ICMR, NATIONAL_FDA")

class GuidelineReferenceItem(BaseModel):
    authority: str              # WHO, CDC, NICE, NATIONAL_ICMR, NATIONAL_FDA
    document_code: str          # e.g., WHO-TRS-961, NICE-NG191, CDC-AMR-2022
    guideline_title: str
    section_reference: str      # e.g., "Sec 4.2, Paragraph 3"
    publication_year: int
    evidence_grade: str         # Grade A, Grade B, Grade C, Strong Recommendation
    recommendation_text: str
    first_line_regimen: str
    contraindications: List[str]

class ClinicalGuidelineResponse(BaseModel):
    condition_name: str
    matched_guidelines_count: int
    guideline_references: List[GuidelineReferenceItem]
    execution_time_ms: int
