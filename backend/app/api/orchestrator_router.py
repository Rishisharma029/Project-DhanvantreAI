import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.utils.prompt_injection_guard import validate_and_sanitize_input
from app.schemas.orchestrator_schema import (
    OrchestratorRequest, ClinicalLLMResponse, PromptPreviewResponse
)
from app.services.llm_orchestrator import (
    build_orchestrator_prompt, orchestrate_llm_pipeline
)

router = APIRouter(prefix="/orchestrator", tags=["LLM Orchestrator Engine"])

@router.post("/generate", response_model=ClinicalLLMResponse)
def generate_clinical_response_endpoint(req: OrchestratorRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Executes full LLM Orchestration Pipeline:
    Prompt Building, Medical Context Injection, Tool Selection & Execution, JSON Parsing, and Clinical Response Generation.
    """
    # Prompt injection check
    user_input = req.query or req.user_message or ""
    sanitized_input, error_msg = validate_and_sanitize_input(user_input)
    if error_msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )
    # Replace with sanitized input
    if req.query:
        req.query = sanitized_input
    if req.user_message:
        req.user_message = sanitized_input

    return orchestrate_llm_pipeline(req, db)

@router.post("/build-prompt", response_model=PromptPreviewResponse)
def build_prompt_endpoint(req: OrchestratorRequest):
    """Inspect generated system prompt, user prompt, and injected medical context."""
    # Prompt injection check
    user_input = req.query or req.user_message or ""
    sanitized_input, error_msg = validate_and_sanitize_input(user_input)
    if error_msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )
    if req.query:
        req.query = sanitized_input
    if req.user_message:
        req.user_message = sanitized_input

    return build_orchestrator_prompt(req)
