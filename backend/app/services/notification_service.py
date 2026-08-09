import sqlite3
from typing import List
from app.schemas.notification_schema import (
    PasswordResetNotificationRequest, ReportReadyNotificationRequest,
    FollowupReminderNotificationRequest, NotificationItemResponse
)

def mock_send_email_transport(to_email: str, subject: str, body_text: str) -> bool:
    """Mock Email Dispatcher Transport Layer for Development & Testing."""
    print(f"[NOTIFICATION SERVICE MOCK EMAIL DISPATCH]")
    print(f"TO: {to_email}")
    print(f"SUBJECT: {subject}")
    print(f"BODY:\n{body_text}\n" + "="*50)
    return True

def dispatch_password_reset_email(req: PasswordResetNotificationRequest, db: sqlite3.Connection) -> NotificationItemResponse:
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?) LIMIT 1;", (req.email,))
    row = cursor.fetchone()
    user_id = row[0] if row else 0

    title = "Password Reset Request"
    message = f"Hello, you requested a password reset. Please use your reset token: {req.reset_token} or click the reset link to reset your account password."

    mock_send_email_transport(req.email, title, message)

    cursor.execute("""
        INSERT INTO user_notifications (user_id, notification_type, title, message, recipient_email, status)
        VALUES (?, 'Password Reset', ?, ?, ?, 'SENT');
    """, (user_id, title, message, req.email))
    db.commit()
    notif_id = cursor.lastrowid

    cursor.execute("SELECT id, user_id, notification_type, title, message, recipient_email, status, sent_at, created_at FROM user_notifications WHERE id = ?;", (notif_id,))
    r = cursor.fetchone()
    return NotificationItemResponse(
        id=r[0], user_id=r[1], notification_type=r[2], title=r[3], message=r[4], recipient_email=r[5], status=r[6], sent_at=str(r[7]), created_at=str(r[8])
    )

def dispatch_report_ready_notification(user_id: int, req: ReportReadyNotificationRequest, db: sqlite3.Connection) -> NotificationItemResponse:
    cursor = db.cursor()
    title = f"Diagnostic Report Ready: {req.report_title}"
    message = f"Good news! Your diagnostic {req.report_type} ('{req.report_title}') has been processed and is now available in your patient portal."

    mock_send_email_transport(req.recipient_email, title, message)

    cursor.execute("""
        INSERT INTO user_notifications (user_id, notification_type, title, message, recipient_email, status)
        VALUES (?, 'Report Ready', ?, ?, ?, 'SENT');
    """, (user_id, title, message, req.recipient_email))
    db.commit()
    notif_id = cursor.lastrowid

    cursor.execute("SELECT id, user_id, notification_type, title, message, recipient_email, status, sent_at, created_at FROM user_notifications WHERE id = ?;", (notif_id,))
    r = cursor.fetchone()
    return NotificationItemResponse(
        id=r[0], user_id=r[1], notification_type=r[2], title=r[3], message=r[4], recipient_email=r[5], status=r[6], sent_at=str(r[7]), created_at=str(r[8])
    )

def dispatch_followup_reminder(user_id: int, req: FollowupReminderNotificationRequest, db: sqlite3.Connection) -> NotificationItemResponse:
    cursor = db.cursor()
    title = f"Upcoming Follow-up Appointment Reminder"
    message = f"Reminder: You have a scheduled clinical follow-up visit with {req.doctor_name} on {req.visit_date} regarding '{req.reason}'."

    mock_send_email_transport(req.recipient_email, title, message)

    cursor.execute("""
        INSERT INTO user_notifications (user_id, notification_type, title, message, recipient_email, status)
        VALUES (?, 'Follow-up Reminder', ?, ?, ?, 'SENT');
    """, (user_id, title, message, req.recipient_email))
    db.commit()
    notif_id = cursor.lastrowid

    cursor.execute("SELECT id, user_id, notification_type, title, message, recipient_email, status, sent_at, created_at FROM user_notifications WHERE id = ?;", (notif_id,))
    r = cursor.fetchone()
    return NotificationItemResponse(
        id=r[0], user_id=r[1], notification_type=r[2], title=r[3], message=r[4], recipient_email=r[5], status=r[6], sent_at=str(r[7]), created_at=str(r[8])
    )

def get_user_notifications_inbox(user_id: int, db: sqlite3.Connection) -> List[NotificationItemResponse]:
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, notification_type, title, message, recipient_email, status, sent_at, created_at FROM user_notifications WHERE user_id = ? ORDER BY created_at DESC;", (user_id,))
    rows = cursor.fetchall()
    return [
        NotificationItemResponse(id=r[0], user_id=r[1], notification_type=r[2], title=r[3], message=r[4], recipient_email=r[5], status=r[6], sent_at=str(r[7]), created_at=str(r[8]))
        for r in rows
    ]
