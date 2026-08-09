from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TopSearchedItem(BaseModel):
    term: str
    category: str # Medicine, Disease, Symptom, General
    search_count: int

class SearchTrendPoint(BaseModel):
    date_str: str # YYYY-MM-DD
    total_searches: int

class AIUsageStatistics(BaseModel):
    total_ai_queries: int
    avg_tools_called: float
    avg_latency_ms: float
    avg_safety_score: float
    emergency_alerts_flagged: int
    emergency_rate_percentage: str

class AnalyticsDashboardResponse(BaseModel):
    total_search_volume: int
    top_medicines: List[TopSearchedItem]
    top_diseases: List[TopSearchedItem]
    search_trends: List[SearchTrendPoint]
    domain_distribution: Dict[str, int]
    ai_usage_statistics: AIUsageStatistics
