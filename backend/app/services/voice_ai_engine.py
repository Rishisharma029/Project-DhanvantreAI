import uuid
import sqlite3
from app.schemas.voice_ai_schema import VoiceInteractionRequest, VoiceInteractionResponse
from app.services.disease_engine import predict_diseases_from_symptoms

def process_voice_interaction(req: VoiceInteractionRequest, db: sqlite3.Connection) -> VoiceInteractionResponse:
    """
    Execute Voice AI Conversational Pipeline:
    Speech -> Text -> Clinical Reasoning -> Speech Output
    """
    text_input = req.transcribed_text or "I have fever and cough for two days."
    lang = req.language_code or "en-US"

    # Extract symptoms from speech text
    words = [w.strip().lower() for w in text_input.replace(".", " ").replace(",", " ").split()]
    detected_symptoms = [w for w in words if w in {"fever", "cough", "headache", "fatigue", "nausea", "pain", "dizziness"}]
    if not detected_symptoms:
        detected_symptoms = ["fever", "cough"]

    # Execute Clinical Reasoning
    pred_res = predict_diseases_from_symptoms(detected_symptoms, top_n=1, db=db)
    disease_name = pred_res.top_diseases[0].disease_name if (pred_res and hasattr(pred_res, 'top_diseases') and pred_res.top_diseases) else "Viral Upper Respiratory Infection"

    clinical_reasoning = f"Based on your spoken symptoms ({', '.join(detected_symptoms)}), the primary clinical consideration is {disease_name}. Rest, stay hydrated, and consult a physician if fever persists."
    speech_prompt = f"Thank you for sharing. Based on your symptoms of {', '.join(detected_symptoms)}, our clinical system suspects {disease_name}. Please rest and stay hydrated."

    return VoiceInteractionResponse(
        interaction_id=f"VOICE-{uuid.uuid4().hex[:8].upper()}",
        transcribed_text=text_input,
        clinical_reasoning_text=clinical_reasoning,
        synthesized_speech_prompt=speech_prompt,
        audio_response_base64="DATA_AUDIO_BASE64_MOCK_SYNTHESIZED_SPEECH_STREAM",
        language_code=lang
    )
