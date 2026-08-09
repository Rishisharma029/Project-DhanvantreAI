import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
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
    return orchestrate_llm_pipeline(req, db)

@router.post("/build-prompt", response_model=PromptPreviewResponse)
def build_prompt_endpoint(req: OrchestratorRequest):
    """Inspect generated system prompt, user prompt, and injected medical context."""
    return build_orchestrator_prompt(req)
