import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.guardrail_schema import (
    GuardrailVerifyRequest, GuardrailVerifyResponse
)
from app.services.llm_guardrail_engine import verify_llm_guardrails

router = APIRouter(prefix="/guardrails", tags=["LLM Guardrail Engine ⭐⭐⭐⭐⭐"])

@router.post("/verify", response_model=GuardrailVerifyResponse)
def verify_guardrails_endpoint(req: GuardrailVerifyRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute LLM Guardrail Safety Audit:
    Verifies Medicine Names, Dosages, Warnings, Contraindications, and Safety Instructions.
    If mismatch/hallucination is detected -> Returns status 'REGENERATE_REQUIRED' with corrective prompt feedback.
    """
    return verify_llm_guardrails(req, db)
