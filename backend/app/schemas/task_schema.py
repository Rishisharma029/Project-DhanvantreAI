from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class TaskEnqueueRequest(BaseModel):
    task_type: str = Field(..., description="pdf_generation, email_sending, database_sync, cache_refresh, ai_preprocessing")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Custom arguments for task worker")
    priority: Optional[str] = "NORMAL" # LOW, NORMAL, HIGH, CRITICAL

class TaskStatusResponse(BaseModel):
    task_id: str
    task_type: str
    status: str # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
    progress_percentage: int = 0
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class ActiveTasksResponse(BaseModel):
    total_active_tasks: int
    tasks: List[TaskStatusResponse]
