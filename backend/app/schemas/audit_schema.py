from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AuditLogItem(BaseModel):
    id: int
    user_id: int
    log_type: str # API_REQUEST, ERROR, AI_CALL, SEARCH_QUERY
    endpoint: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None
    latency_ms: int = 0
    message: Optional[str] = None
    details_json: Optional[str] = "{}"
    created_at: str

class RecommendationHistoryItem(BaseModel):
    id: int
    user_id: int
    session_id: Optional[str] = None
    symptoms_json: str
    disease_recommendations_json: str
    medicine_recommendations_json: str
    safety_warnings_json: str
    created_at: str

class AuditSummaryResponse(BaseModel):
    total_api_requests: int
    total_ai_calls: int
    total_errors_logged: int
    total_searches_logged: int
    total_recommendations_archived: int
