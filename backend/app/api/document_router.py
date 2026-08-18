import re
import os
from fastapi import APIRouter, HTTPException, Header
from app.schemas.document_ai_schema import DocumentAIRequest, DocumentAIResponse
from app.services.document_ai_engine import process_document_ai

router = APIRouter(prefix="/document", tags=["Document AI"])

# Allowed MIME types for document uploads
ALLOWED_DOCUMENT_MIME_TYPES = [
    "application/pdf",
    "image/jpeg", "image/jpg", "image/png", "image/tiff",
    "text/plain",
]

# Allowed file extensions (lowercase)
ALLOWED_DOCUMENT_EXTENSIONS = [
    ".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".txt",
]


def validate_document_upload(filename: str = None) -> None:
    """
    Validate that the uploaded document filename has an allowed extension.
    """
    if not filename:
        return  # No filename provided, skip validation (raw OCR text only)

    _, ext = os.path.splitext(filename.lower())
    if ext and ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported document type: {ext}. Allowed: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
        )


def validate_document_mime(content_type: str = None) -> None:
    """
    Validate that the MIME type is in the whitelist.
    """
    if not content_type:
        return

    mime_lower = content_type.lower().split(";")[0].strip()
    if mime_lower not in ALLOWED_DOCUMENT_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported document MIME type: {mime_lower}. Allowed: {', '.join(ALLOWED_DOCUMENT_MIME_TYPES)}"
        )


@router.post("/analyze", response_model=DocumentAIResponse)
def analyze_document_endpoint(req: DocumentAIRequest, content_type: str = Header(None)):
    """
    Execute Document AI Pipeline:
    Extracts lab entities from prescriptions, blood reports, and other medical documents.
    """
    validate_document_upload(req.file_filename)
    validate_document_mime(content_type)

    try:
        return process_document_ai(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document AI analysis failure: {str(e)}")
