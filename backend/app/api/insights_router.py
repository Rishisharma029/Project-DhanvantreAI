from fastapi import APIRouter, HTTPException
from app.schemas.personalized_insights_schema import PersonalizedInsightsRequest, PersonalizedInsightsResponse
from app.services.personalized_insights_engine import generate_personalized_insights

router = APIRouter(prefix="/insights", tags=["Personalized Health Insights ⭐⭐⭐⭐⭐"])

@router.post("/daily", response_model=PersonalizedInsightsResponse)
def get_daily_personalized_insights(req: PersonalizedInsightsRequest):
    """
    Generate Personalized Daily Health Insights:
    1. Medicine Adherence Reminders
    2. Water & Hydration Goals
    3. Lifestyle & Exercise Suggestions
    4. General Health Education
    """
    try:
        return generate_personalized_insights(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failure: {str(e)}")
