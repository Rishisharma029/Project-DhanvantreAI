from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class DocumentType(str, Enum):
    PRESCRIPTION = "PRESCRIPTION"
    BLOOD_REPORT = "BLOOD_REPORT"
    CBC = "CBC"
    THYROID = "THYROID"
    URINE_TEST = "URINE_TEST"
    MRI_REPORT = "MRI_REPORT"
    ECG_REPORT = "ECG_REPORT"
    GENERAL_LAB = "GENERAL_LAB"

class ExtractedLabEntity(BaseModel):
    biomarker_name: str
    value: str
    unit: str
    normal_range: str
    is_abnormal: bool
    abnormality_flag: Optional[str] = "NORMAL"  # HIGH, LOW, NORMAL, CRITICAL

class DocumentAIRequest(BaseModel):
    document_type: DocumentType = Field(..., json_schema_extra={"example": "CBC"})
    raw_ocr_text: Optional[str] = Field(default=None, json_schema_extra={"example": "COMPLETE BLOOD COUNT: Hemoglobin: 10.2 g/dL (Normal 13.5-17.5). WBC: 12500 /uL (Normal 4500-11000). Platelet Count: 250000 /uL."})
    file_filename: Optional[str] = Field(default="cbc_report_patient.pdf")

class DocumentAIResponse(BaseModel):
    document_id: str
    document_type: DocumentType
    ocr_extracted_text: str
    extracted_entities: List[ExtractedLabEntity]
    clinical_summary: str
    abnormal_flags_count: int
    recommended_clinical_actions: List[str]
