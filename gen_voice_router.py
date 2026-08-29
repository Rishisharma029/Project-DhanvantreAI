"""Generate voice_router.py with proper audio validation"""

content = '''import base64
import re
from fastapi import APIRouter, HTTPException
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
        mime_match = re.match(r"data:([\\w\\-\\+\\.]+/[\\w\\-\\+\\.]+);base64,", data)
        if not mime_match:
            raise HTTPException(
                status_code=400,
                detail="Invalid audio data format. Must be a valid data URI or raw base64."
            )
        mime_type = mime_match.group(1).lower()
        if mime_type not in ALLOWED_AUDIO_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio type: {mime_type}. Allowed: {', '.join(ALLOWED_AUDIO_MIME_TYPES)}"
            )
    else:
        # Raw base64 - validate it's actually valid base64
        try:
            clean_data = data.strip()
            base64.b64decode(clean_data, validate=True)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid base64 audio data."
            )


@router.post("/interact", response_model=VoiceInteractionResponse)
def voice_interact_endpoint(req: VoiceInteractionRequest):
    """
    Execute Voice AI Pipeline:
    Processes transcribed text or audio for symptom analysis.
    """
    if req.audio_base64:
        validate_audio_upload(req.audio_base64)

    try:
        return process_voice_interaction(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice AI interaction failure: {str(e)}")
'''

with open("backend/app/api/voice_router.py", "w", encoding="utf-8") as f:
    f.write(content)

print("voice_router.py generated successfully")
