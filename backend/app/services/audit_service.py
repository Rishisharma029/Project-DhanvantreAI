import sqlite3
import json
from typing import List, Dict, Any
from app.schemas.audit_schema import (
    AuditLogItem, RecommendationHistoryItem, AuditSummaryResponse
)

# 1. LOGGERS
def log_system_audit_event(user_id: int, log_type: str, endpoint: str, method: str, status_code: int, latency_ms: int, message: str, details_json: str, db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO system_audit_logs (user_id, log_type, endpoint, method, status_code, latency_ms, message, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (user_id, log_type, endpoint, method, status_code, latency_ms, message, details_json))
    db.commit()

def log_security_audit_event(user_id: int, event_type: str, message: str, ip_address: str, db: sqlite3.Connection):
    """
    Log security-focused governance audit events.
    Strictly avoids logging sensitive PHI (protected health information), medical data, passwords, or raw tokens.
    Event Types: LOGIN_FAILED, PASSWORD_CHANGED, ROLE_CHANGED, ACCOUNT_LOCKED, JWT_REVOKED, PERMISSION_DENIED.
    """
    cursor = db.cursor()
    details = json.dumps({"ip_address": ip_address, "phi_logged": False})
    cursor.execute("""
        INSERT INTO system_audit_logs (user_id, log_type, endpoint, method, status_code, latency_ms, message, details_json)
        VALUES (?, ?, 'SECURITY_GOVERNANCE', 'SYSTEM', 200, 0, ?, ?);
    """, (user_id, event_type, f"[SECURITY] {message}", details))
    db.commit()


def log_recommendation_history_event(user_id: int, session_id: str, symptoms: Any, diseases: Any, medicines: Any, warnings: Any, db: sqlite3.Connection):
    cursor = db.cursor()
    sym_str = json.dumps(symptoms) if not isinstance(symptoms, str) else symptoms
    dis_str = json.dumps(diseases) if not isinstance(diseases, str) else diseases
    med_str = json.dumps(medicines) if not isinstance(medicines, str) else medicines
    warn_str = json.dumps(warnings) if not isinstance(warnings, str) else warnings

    cursor.execute("""
        INSERT INTO recommendation_history_logs (user_id, session_id, symptoms_json, disease_recommendations_json, medicine_recommendations_json, safety_warnings_json)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (user_id, session_id, sym_str, dis_str, med_str, warn_str))
    db.commit()

# 2. QUERY HELPERS
def get_audit_logs_by_type(log_type: str, limit: int, db: sqlite3.Connection) -> List[AuditLogItem]:
    cursor = db.cursor()
    if log_type and log_type.lower() != "all":
        cursor.execute("""
            SELECT id, user_id, log_type, endpoint, method, status_code, latency_ms, message, details_json, created_at
            FROM system_audit_logs
            WHERE LOWER(log_type) = LOWER(?)
            ORDER BY id DESC
            LIMIT ?;
        """, (log_type, limit))
    else:
        cursor.execute("""
            SELECT id, user_id, log_type, endpoint, method, status_code, latency_ms, message, details_json, created_at
            FROM system_audit_logs
            ORDER BY id DESC
            LIMIT ?;
        """, (limit,))

    rows = cursor.fetchall()
    return [
        AuditLogItem(
            id=r[0], user_id=r[1], log_type=r[2], endpoint=r[3], method=r[4],
            status_code=r[5], latency_ms=r[6], message=r[7], details_json=r[8], created_at=str(r[9])
        ) for r in rows
    ]

def get_recommendation_history(user_id: int, limit: int, db: sqlite3.Connection) -> List[RecommendationHistoryItem]:
    cursor = db.cursor()
    if user_id > 0:
        cursor.execute("""
            SELECT id, user_id, session_id, symptoms_json, disease_recommendations_json, medicine_recommendations_json, safety_warnings_json, created_at
            FROM recommendation_history_logs
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?;
        """, (user_id, limit))
    else:
        cursor.execute("""
            SELECT id, user_id, session_id, symptoms_json, disease_recommendations_json, medicine_recommendations_json, safety_warnings_json, created_at
            FROM recommendation_history_logs
            ORDER BY id DESC
            LIMIT ?;
        """, (limit,))

    rows = cursor.fetchall()
    return [
        RecommendationHistoryItem(
            id=r[0], user_id=r[1], session_id=r[2], symptoms_json=r[3],
            disease_recommendations_json=r[4], medicine_recommendations_json=r[5],
            safety_warnings_json=r[6], created_at=str(r[7])
        ) for r in rows
    ]

def get_audit_summary_metrics(db: sqlite3.Connection) -> AuditSummaryResponse:
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM system_audit_logs WHERE log_type = 'API_REQUEST';")
    api_cnt = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM system_audit_logs WHERE log_type = 'AI_CALL';")
    ai_cnt = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM system_audit_logs WHERE log_type = 'ERROR' OR status_code >= 400;")
    err_cnt = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM system_audit_logs WHERE log_type = 'SEARCH_QUERY';")
    srch_cnt = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM recommendation_history_logs;")
    rec_cnt = cursor.fetchone()[0] or 0

    return AuditSummaryResponse(
        total_api_requests=api_cnt,
        total_ai_calls=ai_cnt,
        total_errors_logged=err_cnt,
        total_searches_logged=srch_cnt,
        total_recommendations_archived=rec_cnt
    )
