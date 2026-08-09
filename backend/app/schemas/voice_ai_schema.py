from typing import Optional
from pydantic import BaseModel, Field

class VoiceInteractionRequest(BaseModel):
    audio_base64: Optional[str] = Field(default=None)
    transcribed_text: Optional[str] = Field(default=None, json_schema_extra={"example": "Doctor, I have had a fever and dry cough for two days."})
    language_code: Optional[str] = Field(default="en-US")

class VoiceInteractionResponse(BaseModel):
    interaction_id: str
    transcribed_text: str
    clinical_reasoning_text: str
    synthesized_speech_prompt: str
    audio_response_base64: Optional[str]
    language_code: str
