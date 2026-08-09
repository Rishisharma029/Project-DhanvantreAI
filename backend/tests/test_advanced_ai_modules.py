import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_user_db
from app.services.followup_ai_engine import process_followup_assessment
from app.services.document_ai_engine import process_document_ai
from app.services.voice_ai_engine import process_voice_interaction
from app.services.image_ai_engine import process_image_ai_analysis
from app.schemas.followup_ai_schema import FollowUpAssessmentRequest
from app.schemas.document_ai_schema import DocumentAIRequest, DocumentType
from app.schemas.voice_ai_schema import VoiceInteractionRequest
from app.schemas.image_ai_schema import ImageAIRequest, ImageType

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_user_db()

def test_followup_ai_assessment():
    """Verify follow-up assessment updates triage and clinical progression status."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = FollowUpAssessmentRequest(
        session_id="SESS-001",
        feeling_better=True,
        resolved_symptoms=["fever"]
    )
    res = process_followup_assessment(req, conn)
    conn.close()

    assert res.progression_status.value in ("IMPROVING", "RESOLVED")
    assert res.updated_risk_level == "LOW_GREEN"
    assert len(res.recommended_actions) >= 2

def test_document_ai_ocr_extraction():
    """Verify OCR & Document AI extracts lab entities and flags abnormal values."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = DocumentAIRequest(
        document_type=DocumentType.CBC,
        raw_ocr_text="CBC: Hemoglobin 10.2 g/dL (Normal 13.5-17.5). WBC 12500 /uL."
    )
    res = process_document_ai(req, conn)
    conn.close()

    assert res.document_type == DocumentType.CBC
    assert len(res.extracted_entities) >= 3
    assert res.abnormal_flags_count >= 1

def test_voice_ai_speech_reasoning():
    """Verify Voice AI Speech -> Text -> Reasoning -> Speech pipeline."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    req = VoiceInteractionRequest(transcribed_text="I have fever and cough for two days.")
    res = process_voice_interaction(req, conn)
    conn.close()

    assert "fever" in res.transcribed_text
    assert len(res.clinical_reasoning_text) > 20
    assert "synthesized_speech_prompt" in res.__dict__ or hasattr(res, 'synthesized_speech_prompt')

def test_image_ai_disclaimer_and_analysis():
    """Verify Multi-Modal Image AI and enforcement of mandatory clinical disclaimer."""
    req = ImageAIRequest(
        image_type=ImageType.SKIN_RASH,
        image_base64_or_path="data:image/jpeg;base64,mock"
    )
    res = process_image_ai_analysis(req)

    assert res.image_type == ImageType.SKIN_RASH
    assert len(res.detected_features) >= 2
    assert "DISCLAIMER:" in res.disclaimer

def test_advanced_ai_rest_endpoints():
    """Test HTTP REST endpoints for FollowUp, Document AI, Voice AI, and Image AI."""
    # 1. FollowUp REST
    f_res = client.post(f"{settings.API_V1_STR}/followup/assess", json={"session_id": "S1", "feeling_better": True})
    assert f_res.status_code == 200
    assert "progression_status" in f_res.json()

    # 2. Document AI REST
    d_res = client.post(f"{settings.API_V1_STR}/document/analyze", json={"document_type": "CBC"})
    assert d_res.status_code == 200
    assert "extracted_entities" in d_res.json()

    # 3. Voice AI REST
    v_res = client.post(f"{settings.API_V1_STR}/voice/interact", json={"transcribed_text": "I have fever"})
    assert v_res.status_code == 200
    assert "clinical_reasoning_text" in v_res.json()

    # 4. Image AI REST
    i_res = client.post(f"{settings.API_V1_STR}/image/analyze", json={"image_type": "SKIN_RASH", "image_base64_or_path": "mock"})
    assert i_res.status_code == 200
    assert "disclaimer" in i_res.json()
