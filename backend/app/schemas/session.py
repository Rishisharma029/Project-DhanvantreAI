from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SessionCreate(BaseModel):
    title: Optional[str] = "New Consultation"

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)
    metadata: Optional[Dict[str, Any]] = {}

class MessageResponse(BaseModel):
    id: int
    session_id: int
    sender: str
    content: str
    metadata: Dict[str, Any] = {}
    created_at: str

class SessionResponse(BaseModel):
    id: int
    session_uuid: str
    user_id: int
    title: str
    is_active: bool
    is_timed_out: bool = False
    last_activity_at: str
    created_at: str
    message_count: int = 0

class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse] = []
    ai_context_memory: List[Dict[str, str]] = []
