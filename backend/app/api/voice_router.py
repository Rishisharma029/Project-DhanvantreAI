import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.voice_ai_schema import VoiceInteractionRequest, VoiceInteractionResponse
from app.services.voice_ai_engine import process_voice_interaction

router = APIRouter(prefix="/voice", tags=["Voice AI ⭐⭐⭐⭐⭐"])

@router.post("/interact", response_model=VoiceInteractionResponse)
def voice_interaction_endpoint(req: VoiceInteractionRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute Voice AI Conversational Pipeline:
    Speech -> Text -> Clinical Reasoning -> Speech Output.
    Supports natural, hands-free patient & physician consultations.
    """
    try:
        return process_voice_interaction(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice AI interaction failure: {str(e)}")
