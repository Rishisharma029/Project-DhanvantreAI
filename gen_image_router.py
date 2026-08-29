"""Generate image_router.py with proper byte literals"""

# Use bytes literals defined via hex to avoid encoding issues
jpeg_magic = bytes.fromhex("FFD8FF")
png_magic = bytes.fromhex("89504E47")
gif87_magic = bytes.fromhex("474946383761")
gif89_magic = bytes.fromhex("474946383961")
bmp_magic = bytes.fromhex("424D")
riff_magic = bytes.fromhex("52494646")
webp_magic = bytes.fromhex("57454250")

content = f'''import base64
import re
from fastapi import APIRouter, HTTPException
from app.schemas.image_ai_schema import ImageAIRequest, ImageAIResponse
from app.services.image_ai_engine import process_image_ai_analysis

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
        mime_match = re.match(r"data:([\\w\\-\\+\\.]+/[\\w\\-\\+\\.]+);base64,", data)
        if not mime_match:
            raise HTTPException(
                status_code=400,
                detail="Invalid image data format. Must be a valid data URI or raw base64."
            )
        mime_type = mime_match.group(1).lower()
        if mime_type not in ALLOWED_IMAGE_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image type: {{mime_type}}. Allowed: {{', '.join(ALLOWED_IMAGE_MIME_TYPES)}}"
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
        if decoded[:3] == {jpeg_magic!r}:
            pass  # JPEG OK
        elif decoded[:4] == {png_magic!r}:
            pass  # PNG OK
        elif decoded[:4] == {riff_magic!r} and len(decoded) > 12 and decoded[8:12] == {webp_magic!r}:
            pass  # WEBP OK
        elif decoded[:6] in ({gif87_magic!r}, {gif89_magic!r}):
            pass  # GIF OK
        elif decoded[:2] == {bmp_magic!r}:
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

    try:
        return process_image_ai_analysis(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image AI analysis failure: {{str(e)}}")
'''

with open("backend/app/api/image_router.py", "w", encoding="utf-8") as f:
    f.write(content)

print("image_router.py generated successfully")
