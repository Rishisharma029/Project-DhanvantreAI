from fastapi import APIRouter, HTTPException
from app.schemas.quality_evaluation_schema import QualityEvaluationRequest, QualityEvaluationResponse
from app.services.quality_evaluation_engine import evaluate_ai_quality

router = APIRouter(prefix="/quality", tags=["AI Quality Evaluation ⭐⭐⭐⭐⭐"])

@router.post("/evaluate", response_model=QualityEvaluationResponse)
def evaluate_ai_quality_endpoint(req: QualityEvaluationRequest):
    """
    Automated 5-Metric AI Quality Evaluation Engine:
    Measures Faithfulness, Groundedness, Citation Coverage, Consistency, and Safety.
    Generates Quality Score (0-100), Quality Grade, Approval Status, and Remediation Actions.
    """
    try:
        return evaluate_ai_quality(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quality Evaluation failure: {str(e)}")
