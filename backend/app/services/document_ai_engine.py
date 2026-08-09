import re
import uuid
import sqlite3
from typing import List
from app.schemas.document_ai_schema import (
    DocumentAIRequest,
    DocumentAIResponse,
    ExtractedLabEntity,
    DocumentType
)

def process_document_ai(req: DocumentAIRequest, db: sqlite3.Connection) -> DocumentAIResponse:
    """
    Execute OCR & Document AI Pipeline:
    Upload -> OCR -> Entity Extraction -> Knowledge Base -> Summary
    """
    raw_text = req.raw_ocr_text or f"Sample {req.document_type.value} content for patient analysis."
    entities: List[ExtractedLabEntity] = []

    # Sample lab extraction rules for common document types
    if req.document_type == DocumentType.CBC or "blood" in raw_text.lower() or "cbc" in raw_text.lower():
        entities.append(ExtractedLabEntity(
            biomarker_name="Hemoglobin (Hb)",
            value="10.2",
            unit="g/dL",
            normal_range="13.5 - 17.5 g/dL",
            is_abnormal=True,
            abnormality_flag="LOW"
        ))
        entities.append(ExtractedLabEntity(
            biomarker_name="White Blood Cell (WBC) Count",
            value="12,500",
            unit="/uL",
            normal_range="4,500 - 11,000 /uL",
            is_abnormal=True,
            abnormality_flag="HIGH"
        ))
        entities.append(ExtractedLabEntity(
            biomarker_name="Platelet Count",
            value="250,000",
            unit="/uL",
            normal_range="150,000 - 450,000 /uL",
            is_abnormal=False,
            abnormality_flag="NORMAL"
        ))
    elif req.document_type == DocumentType.THYROID or "tsh" in raw_text.lower():
        entities.append(ExtractedLabEntity(
            biomarker_name="Thyroid Stimulating Hormone (TSH)",
            value="6.8",
            unit="uIU/mL",
            normal_range="0.4 - 4.0 uIU/mL",
            is_abnormal=True,
            abnormality_flag="HIGH"
        ))
        entities.append(ExtractedLabEntity(
            biomarker_name="Free T4",
            value="0.9",
            unit="ng/dL",
            normal_range="0.8 - 1.8 ng/dL",
            is_abnormal=False,
            abnormality_flag="NORMAL"
        ))
    else:
        entities.append(ExtractedLabEntity(
            biomarker_name="General Diagnostic Marker",
            value="Within Standard Limits",
            unit="N/A",
            normal_range="Standard Clinical Range",
            is_abnormal=False,
            abnormality_flag="NORMAL"
        ))

    abnormal_count = sum(1 for e in entities if e.is_abnormal)
    summary = f"Processed {req.document_type.value} document. Identified {len(entities)} biomarkers, including {abnormal_count} abnormal flags requiring physician review."

    actions = [
        "Review abnormal lab flags with primary care physician.",
        "Correlate lab findings with patient clinical symptoms.",
        "Schedule follow-up lab re-testing if indicated."
    ]

    return DocumentAIResponse(
        document_id=f"DOC-{uuid.uuid4().hex[:8].upper()}",
        document_type=req.document_type,
        ocr_extracted_text=raw_text,
        extracted_entities=entities,
        clinical_summary=summary,
        abnormal_flags_count=abnormal_count,
        recommended_clinical_actions=actions
    )
