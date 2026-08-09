from fastapi import APIRouter, status
from typing import Dict, Any
from app.services.ai_eval_dashboard_service import ai_eval_dashboard_service

router = APIRouter(prefix="/ai-evaluation", tags=["AI Quality & Safety Evaluation Dashboard"])

@router.get("/dashboard-stats", status_code=status.HTTP_200_OK)
def get_ai_evaluation_dashboard_stats() -> Dict[str, Any]:
    """
    Real-time AI Quality & Evaluation Telemetry API.
    Provides Hallucination Rate, Citation Coverage, Groundedness, Faithfulness, and Safety Scores.
    """
    return ai_eval_dashboard_service.get_dashboard_metrics()
