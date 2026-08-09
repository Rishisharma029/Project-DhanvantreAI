from fastapi import APIRouter, HTTPException
from app.schemas.image_ai_schema import ImageAIRequest, ImageAIResponse
from app.services.image_ai_engine import process_image_ai_analysis

router = APIRouter(prefix="/image", tags=["Image AI ⭐⭐⭐⭐⭐"])

@router.post("/analyze", response_model=ImageAIResponse)
def analyze_medical_image_endpoint(req: ImageAIRequest):
    """
    Execute Multi-Modal Image AI Pipeline:
    Analyzes Skin Rashes, Medication Labels, Pill Identification, and Wound Progression.
    Appends mandatory non-definitive clinical disclaimers.
    """
    try:
        return process_image_ai_analysis(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image AI analysis failure: {str(e)}")
