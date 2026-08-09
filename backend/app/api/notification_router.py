import sqlite3
from typing import List
from fastapi import APIRouter, Depends
from app.database import get_db
from app.api.auth_router import get_current_user
from app.schemas.notification_schema import (
    PasswordResetNotificationRequest, ReportReadyNotificationRequest,
    FollowupReminderNotificationRequest, NotificationItemResponse
)
from app.services.notification_service import (
    dispatch_password_reset_email,
    dispatch_report_ready_notification,
    dispatch_followup_reminder,
    get_user_notifications_inbox
)

router = APIRouter(prefix="/notifications", tags=["Notification Service"])

@router.post("/send-password-reset", response_model=NotificationItemResponse)
def send_password_reset_endpoint(req: PasswordResetNotificationRequest, db: sqlite3.Connection = Depends(get_db)):
    """Dispatch transactional password reset token email."""
    return dispatch_password_reset_email(req, db)

@router.post("/send-report-ready", response_model=NotificationItemResponse)
def send_report_ready_endpoint(req: ReportReadyNotificationRequest, current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Dispatch diagnostic report ready alert notification."""
    return dispatch_report_ready_notification(current_user["id"], req, db)

@router.post("/send-followup-reminder", response_model=NotificationItemResponse)
def send_followup_reminder_endpoint(req: FollowupReminderNotificationRequest, current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Dispatch appointment reminder notification for upcoming clinical follow-up visit."""
    return dispatch_followup_reminder(current_user["id"], req, db)

@router.get("/my-notifications", response_model=List[NotificationItemResponse])
def get_my_notifications_endpoint(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve patient's in-app notification inbox history."""
    return get_user_notifications_inbox(current_user["id"], db)
