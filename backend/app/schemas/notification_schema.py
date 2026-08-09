from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class PasswordResetNotificationRequest(BaseModel):
    email: str = Field(..., description="Registered patient email address")
    reset_token: str = Field(..., description="Secure password reset token")

class ReportReadyNotificationRequest(BaseModel):
    report_title: str = Field(..., min_length=1, description="Title of report e.g. 'Complete Blood Count'")
    report_type: str = Field("Lab Report", description="Type of diagnostic report")
    recipient_email: str = Field(..., description="Recipient email address")

class FollowupReminderNotificationRequest(BaseModel):
    doctor_name: str = Field(..., min_length=1, description="Doctor or clinic name")
    visit_date: str = Field(..., description="Scheduled visit date YYYY-MM-DD")
    reason: str = Field(..., description="Consultation reason")
    recipient_email: str = Field(..., description="Recipient email address")

class NotificationItemResponse(BaseModel):
    id: int
    user_id: int
    notification_type: str
    title: str
    message: str
    recipient_email: str
    status: str
    sent_at: str
    created_at: str
