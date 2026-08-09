from fastapi import APIRouter, HTTPException, Query
from app.schemas.task_schema import TaskEnqueueRequest, TaskStatusResponse, ActiveTasksResponse
from app.services.background_task_queue import task_queue_engine

router = APIRouter(prefix="/tasks", tags=["Background Task Queue"])

@router.post("/enqueue", response_model=TaskStatusResponse)
def enqueue_background_task(req: TaskEnqueueRequest):
    """
    Enqueue an asynchronous background task:
    - pdf_generation
    - email_sending
    - database_sync
    - cache_refresh
    - ai_preprocessing
    """
    allowed_tasks = ["pdf_generation", "email_sending", "database_sync", "cache_refresh", "ai_preprocessing"]
    if req.task_type.lower() not in allowed_tasks:
        raise HTTPException(status_code=400, detail=f"Invalid task_type. Allowed task types: {allowed_tasks}")

    return task_queue_engine.enqueue_task(req.task_type, req.payload, req.priority or "NORMAL")

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def get_task_status_endpoint(task_id: str):
    """Check status, progress, and result of a background task."""
    status = task_queue_engine.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found.")
    return status

@router.get("/active", response_model=ActiveTasksResponse)
def get_active_tasks_endpoint():
    """Retrieve all active (PENDING/RUNNING) background tasks."""
    return task_queue_engine.get_active_tasks()

@router.post("/cancel/{task_id}")
def cancel_task_endpoint(task_id: str):
    """Cancel a pending or running background task."""
    success = task_queue_engine.cancel_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail=f"Task ID {task_id} could not be cancelled or does not exist.")
    return {"message": f"Task ID {task_id} cancelled successfully", "status": "CANCELLED"}
