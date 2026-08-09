import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.document_ai_schema import DocumentAIRequest, DocumentAIResponse
from app.services.document_ai_engine import process_document_ai

router = APIRouter(prefix="/document", tags=["OCR & Document AI ⭐⭐⭐⭐⭐"])

@router.post("/analyze", response_model=DocumentAIResponse)
def analyze_medical_document_endpoint(req: DocumentAIRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute OCR & Medical Document AI Pipeline:
    Upload -> OCR -> Entity Extraction -> Knowledge Base -> Summary.
    Processes Prescriptions, Blood Reports, CBC, Thyroid, Urine, MRI, and ECG reports.
    """
    try:
        return process_document_ai(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document AI analysis failure: {str(e)}")
