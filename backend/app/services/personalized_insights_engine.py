import uuid
import datetime
from typing import List
from app.schemas.personalized_insights_schema import (
    PersonalizedInsightsRequest,
    PersonalizedInsightsResponse,
    HealthInsightItem,
    InsightCategory,
    InsightPriority
)

def generate_personalized_insights(req: PersonalizedInsightsRequest) -> PersonalizedInsightsResponse:
    """
    Generate Personalized Daily Health Insights:
    1. Medicine Adherence Reminders
    2. Water & Hydration Goals
    3. Lifestyle & Exercise Suggestions
    4. General Health Education
    """
    today_str = datetime.date.today().isoformat()
    insights: List[HealthInsightItem] = []

    # 1. Medicine Adherence
    meds = req.current_medications if req.current_medications else ["Prescribed Daily Medication"]
    for i, med in enumerate(meds, 1):
        insights.append(HealthInsightItem(
            insight_id=f"INS-MED-{i:02d}",
            category=InsightCategory.MEDICINE_ADHERENCE,
            title=f"💊 Dose Reminder: {med}",
            description=f"Take your scheduled morning dose of {med} after meals with water.",
            action_prompt="Mark dose as taken",
            priority=InsightPriority.HIGH,
            timestamp="08:00 AM"
        ))

    # 2. Water Hydration Reminder
    insights.append(HealthInsightItem(
        insight_id="INS-H2O-01",
        category=InsightCategory.WATER_HYDRATION,
        title="💧 Daily Hydration Milestone",
        description="Target: 2.5 to 3.0 Liters of water daily. Drink 250ml every 2 hours to maintain optimal physiological kidney function.",
        action_prompt="Log water intake (+250ml)",
        priority=InsightPriority.DAILY_ROUTINE,
        timestamp="10:00 AM"
    ))

    # 3. Lifestyle & Exercise Suggestions
    conditions = [c.lower() for c in (req.chronic_conditions or [])]
    lifestyle_desc = "Engage in 30 minutes of brisk walking or moderate aerobic exercise today."
    if "hypertension" in conditions:
        lifestyle_desc = "Maintain a low-sodium DASH diet (< 2,000mg sodium) and practice 15 minutes of deep breathing relaxation."
    elif "diabetes" in conditions:
        lifestyle_desc = "Perform a post-meal 15-minute walk to optimize glucose metabolism and blood sugar stability."

    insights.append(HealthInsightItem(
        insight_id="INS-LIFE-01",
        category=InsightCategory.LIFESTYLE_SUGGESTION,
        title="🥗 Personalized Lifestyle Goal",
        description=lifestyle_desc,
        action_prompt="View activity guidance",
        priority=InsightPriority.MEDIUM,
        timestamp="02:00 PM"
    ))

    # 4. General Health Education
    insights.append(HealthInsightItem(
        insight_id="INS-EDU-01",
        category=InsightCategory.HEALTH_EDUCATION,
        title="🧠 Medical Wellness Insight: Sleep Hygiene",
        description="7-8 hours of uninterrupted nocturnal sleep enhances cellular immune repair and cognitive memory consolidation.",
        action_prompt="Read evidence article",
        priority=InsightPriority.MEDIUM,
        timestamp="08:00 PM"
    ))

    return PersonalizedInsightsResponse(
        user_id=req.user_id,
        date=today_str,
        total_insights=len(insights),
        insights=insights
    )
