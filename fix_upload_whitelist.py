"""Script to add upload type whitelisting to image, document, and voice routers"""

import os

base_dir = r"backend/app/api"

# === Image Router ===
image_path = os.path.join(base_dir, "image_router.py")
with open(image_path, "r", encoding="utf-8") as f:
    image_content = f.read()

new_image_content = '''import base64
import re
from fastapi import APIRouter, HTTPException
from app.config import settings
from app.schemas.image_ai_schema import ImageAIRequest, ImageAIResponse
from app.services.image_ai_engine import process_image_ai_analysis

router = APIRouter(prefix="/image", tags=["Image AI"])

# Allowed MIME type prefixes for image data URIs
ALLOWED_IMAGE_MIME_PREFIXES = [
    "image/jpeg", "image/jpg", "image/png", "image/webp",
    "image/heic", "image/heif", "image/tiff", "image/bmp", "image/gif",
]

# Allowed file extensions (lowercase)
ALLOWED_IMAGE_EXTENSIONS = [
    ".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".tiff", ".bmp", ".gif",
]


def validate_image_upload(data: str) -> None:
    """
    Validate that the uploaded image data is an allowed type.
    Supports both data URI format (data:image/jpeg;base64,...) and raw base64.
    """
    # Check data URI format
    if data.startswith("data:"):
        mime_match = re.match(r"data:([\w\-\+\.]+/[\w\-\+\.]+);base64,", data)
        if not mime_match:
            raise HTTPException(
                status_code=400,
                detail="Invalid image data format. Must be a valid data URI or raw base64."
            )
        mime_type = mime_match.group(1).lower()
        if mime_type not in ALLOWED_IMAGE_MIME_PREFIXES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image type: {mime_type}. Allowed types: {', '.join(ALLOWED_IMAGE_MIME_PREFIXES)}"
            )
    else:
        # Raw base64 - validate by checking magic bytes after decoding
        try:
            # Strip whitespace
            clean_data = data.strip()
            decoded = base64.b64decode(clean_data, validate=True)
            # Check JPEG magic bytes (FF D8 FF)
            if decoded[:3] == b'\xff\xd8\xff':
                pass  # JPEG OK
            # Check PNG magic bytes (89 50 4E 47)
            elif decoded[:4] == b'\x89PNG':
                pass  # PNG OK
            # Check WEBP magic bytes (RIFF...WEBP)
            elif decoded[:4] == b'RIFF' and decoded[8:12] == b'WEBP':
                pass  # WEBP OK
            # Check GIF magic bytes (GIF87a or GIF89a)
            elif decoded[:6] in (b'GIF87a', b'GIF89a'):
                pass  # GIF OK
            # Check BMP magic bytes (BM)
            elif decoded[:2] == b'BM':
                pass  # BMP OK
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unrecognized image format. Only JPEG, PNG, WEBP, GIF, BMP, HEIC, TIFF are allowed."
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=400,
                detail="Invalid base64 image data. Could not decode or identify image type."
            )


@router.post("/analyze", response_model=ImageAIResponse)
def analyze_medical_image_endpoint(req: ImageAIRequest):
    """
    Execute Multi-Modal Image AI Pipeline:
    Analyzes Skin Rashes, Medication Labels, Pill Identification, and Wound Progression.
    Appends mandatory non-definitive clinical disclaimers.
    """
    # Validate upload type whitelist
    validate_image_upload(req.image_base64_or_path)

    try:
        return process_image_ai_analysis(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image AI analysis failure: {str(e)}")
'''

with open(image_path, "w", encoding="utf-8") as f:
    f.write(new_image_content)

print("image_router.py updated")

# === Document Router ===
document_path = os.path.join(base_dir, "document_router.py")
with open(document_path, "r", encoding="utf-8") as f:
    doc_content = f.read()

new_doc_content = '''import re
from fastapi import APIRouter, HTTPException
from app.config import settings
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

    import os
    _, ext = os.path.splitext(filename.lower())
    if ext and ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported document type: {ext}. Allowed types: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
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
            detail=f"Unsupported document MIME type: {mime_lower}. Allowed types: {', '.join(ALLOWED_DOCUMENT_MIME_TYPES)}"
        )


@router.post("/analyze", response_model=DocumentAIResponse)
def analyze_document_endpoint(req: DocumentAIRequest, content_type: str = None):
    """
    Execute Document AI Pipeline:
    Extracts lab entities from prescriptions, blood reports, and other medical documents.
    """
    # Validate upload type whitelist
    validate_document_upload(req.file_filename)
    validate_document_mime(content_type)

    try:
        return process_document_ai(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document AI analysis failure: {str(e)}")
'''

with open(document_path, "w", encoding="utf-8") as f:
    f.write(new_doc_content)

print("document_router.py updated")

# === Voice Router ===
voice_path = os.path.join(base_dir, "voice_router.py")
with open(voice_path, "r", encoding="utf-8") as f:
    voice_content = f.read()

new_voice_content = '''import base64
import re
from fastapi import APIRouter, HTTPException
from app.config import settings
from app.schemas.voice_ai_schema import VoiceInteractionRequest, VoiceInteractionResponse
from app.services.voice_ai_engine import process_voice_interaction

router = APIRouter(prefix="/voice", tags=["Voice AI"])

# Allowed audio MIME types
ALLOWED_AUDIO_MIME_TYPES = [
    "audio/wav", "audio/mpeg", "audio/mp3", "audio/webm",
    "audio/ogg", "audio/flac", "audio/aac",
]


def validate_audio_upload(data: str) -> None:
    """
    Validate that the uploaded audio data is an allowed type.
    Supports data URI format (data:audio/wav;base64,...) and raw base64.
    """
    if data.startswith("data:"):
        mime_match = re.match(r"data:([\w\-\+\.]+/[\w\-\+\.]+);base64,", data)
        if not mime_match:
            raise HTTPException(
                status_code=400,
                detail="Invalid audio data format. Must be a valid data URI or raw base64."
            )
        mime_type = mime_match.group(1).lower()
        if mime_type not in ALLOWED_AUDIO_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio type: {mime_type}. Allowed types: {', '.join(ALLOWED_AUDIO_MIME_TYPES)}"
            )
    else:
        # Raw base64 - validate it's actually valid base64
        try:
            clean_data = data.strip()
            base64.b64decode(clean_data, validate=True)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=400,
                detail="Invalid base64 audio data. Could not decode."
            )


@router.post("/interact", response_model=VoiceInteractionResponse)
def voice_interact_endpoint(req: VoiceInteractionRequest, db=None):
    """
    Execute Voice AI Pipeline:
    Processes transcribed text or audio for symptom analysis.
    """
    # Validate audio upload type if present
    if req.audio_base64:
        validate_audio_upload(req.audio_base64)

    try:
        return process_voice_interaction(req, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice AI interaction failure: {str(e)}")
'''

with open(voice_path, "w", encoding="utf-8") as f:
    f.write(new_voice_content)

print("voice_router.py updated")
