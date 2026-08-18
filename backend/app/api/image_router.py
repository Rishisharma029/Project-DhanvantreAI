import base64
import re
from fastapi import APIRouter, HTTPException, status
from app.schemas.image_ai_schema import ImageAIRequest, ImageAIResponse
from app.services.image_ai_engine import process_image_ai_analysis
from app.utils.prompt_injection_guard import validate_and_sanitize_input

router = APIRouter(prefix="/image", tags=["Image AI"])

# Allowed MIME types for image data URIs
ALLOWED_IMAGE_MIME_TYPES = [
    "image/jpeg", "image/jpg", "image/png", "image/webp",
    "image/heic", "image/heif", "image/tiff", "image/bmp", "image/gif",
]

def validate_image_upload(data: str) -> None:
    """
    Validate that the uploaded image data is an allowed type.
    Supports data URI format (data:image/jpeg;base64,...) and raw base64.
    Checks magic bytes for raw base64.
    """
    if data.startswith("data:"):
        mime_match = re.match(r"data:([\w\-\+\.]+/[\w\-\+\.]+);base64,", data)
        if not mime_match:
            raise HTTPException(
                status_code=400,
                detail="Invalid image data format. Must be a valid data URI or raw base64."
            )
        mime_type = mime_match.group(1).lower()
        if mime_type not in ALLOWED_IMAGE_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image type: {mime_type}. Allowed: {', '.join(ALLOWED_IMAGE_MIME_TYPES)}"
            )
    else:
        # Raw base64 - validate by checking magic bytes after decoding
        try:
            clean_data = data.strip()
            decoded = base64.b64decode(clean_data, validate=True)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid base64 image data."
            )
        if not decoded:
            raise HTTPException(status_code=400, detail="Empty image data.")
        if decoded[:3] == b'\xff\xd8\xff':
            pass  # JPEG OK
        elif decoded[:4] == b'\x89PNG':
            pass  # PNG OK
        elif decoded[:4] == b'RIFF' and len(decoded) > 12 and decoded[8:12] == b'WEBP':
            pass  # WEBP OK
        elif decoded[:6] in (b'GIF87a', b'GIF89a'):
            pass  # GIF OK
        elif decoded[:2] == b'BM':
            pass  # BMP OK
        else:
            raise HTTPException(
                status_code=400,
                detail="Unrecognized image format. Only JPEG, PNG, WEBP, GIF, BMP are allowed."
            )


@router.post("/analyze", response_model=ImageAIResponse)
def analyze_medical_image_endpoint(req: ImageAIRequest):
    """
    Execute Multi-Modal Image AI Pipeline:
    Analyzes Skin Rashes, Medication Labels, Pill Identification, and Wound Progression.
    Appends mandatory non-definitive clinical disclaimers.
    """
    validate_image_upload(req.image_base64_or_path)

    # Prompt injection check on clinical context
    if req.clinical_context:
        sanitized_context, error_msg = validate_and_sanitize_input(req.clinical_context)
        if error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg,
            )
        req.clinical_context = sanitized_context

    try:
        return process_image_ai_analysis(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image AI analysis failure: {str(e)}")
