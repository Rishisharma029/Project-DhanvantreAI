import uuid
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.session import (
    SessionCreate, MessageCreate, MessageResponse,
    SessionResponse, SessionDetailResponse
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/sessions", tags=["Session & Conversation Manager"])

SESSION_TIMEOUT_MINUTES = 60 # Session inactivity threshold

def check_is_timed_out(last_activity_str: str) -> bool:
    """Check if session has timed out due to inactivity."""
    if not last_activity_str:
        return False
    try:
        last_dt = datetime.fromisoformat(last_activity_str)
        if last_dt.tzinfo is None:
            last_dt = last_dt.replace(tzinfo=timezone.utc)
        now_dt = datetime.now(timezone.utc)
        return (now_dt - last_dt) > timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    except Exception:
        return False

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session_in: SessionCreate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Create a new consultation chat session."""
    session_uuid = str(uuid.uuid4())
    now_str = datetime.now(timezone.utc).isoformat()
    cursor = db.cursor()
    
    cursor.execute("""
        INSERT INTO chat_sessions (session_uuid, user_id, title, is_active, last_activity_at, created_at)
        VALUES (?, ?, ?, 1, ?, ?);
    """, (session_uuid, current_user["id"], session_in.title or "New Consultation", now_str, now_str))
    session_id = cursor.lastrowid
    db.commit()

    cursor.execute("SELECT * FROM chat_sessions WHERE id = ?;", (session_id,))
    row = dict(cursor.fetchone())
    row["is_active"] = bool(row["is_active"])
    row["is_timed_out"] = False
    row["message_count"] = 0
    return row

@router.get("", response_model=list[SessionResponse])
def list_user_sessions(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """List all active and past consultation chat sessions for current user."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT s.*, COUNT(m.id) as message_count
        FROM chat_sessions s
        LEFT JOIN chat_messages m ON s.id = m.session_id
        WHERE s.user_id = ?
        GROUP BY s.id
        ORDER BY s.last_activity_at DESC;
    """, (current_user["id"],))
    
    results = []
    for row in cursor.fetchall():
        d = dict(row)
        d["is_active"] = bool(d["is_active"])
        d["is_timed_out"] = check_is_timed_out(d["last_activity_at"])
        results.append(d)
    return results

@router.get("/{session_uuid}", response_model=SessionDetailResponse)
def resume_session(session_uuid: str, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Resume a consultation session and retrieve full message history and AI context memory."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chat_sessions WHERE session_uuid = ? AND user_id = ?;", (session_uuid, current_user["id"]))
    session_row = cursor.fetchone()
    if not session_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")

    s_dict = dict(session_row)
    s_dict["is_active"] = bool(s_dict["is_active"])
    s_dict["is_timed_out"] = check_is_timed_out(s_dict["last_activity_at"])

    # Fetch messages
    cursor.execute("SELECT * FROM chat_messages WHERE session_id = ? ORDER BY id ASC;", (s_dict["id"],))
    msg_rows = cursor.fetchall()
    
    messages = []
    ai_context_memory = []
    for m in msg_rows:
        m_dict = dict(m)
        try:
            m_dict["metadata"] = json.loads(m_dict["metadata"]) if isinstance(m_dict["metadata"], str) else {}
        except Exception:
            m_dict["metadata"] = {}
        messages.append(m_dict)

        # Format AI Context Memory window
        role_tag = "user" if m_dict["sender"] == "user" else ("assistant" if m_dict["sender"] == "assistant" else "system")
        ai_context_memory.append({
            "role": role_tag,
            "content": m_dict["content"]
        })

    s_dict["message_count"] = len(messages)
    s_dict["messages"] = messages
    s_dict["ai_context_memory"] = ai_context_memory
    return s_dict

@router.post("/{session_uuid}/messages", response_model=MessageResponse)
def append_message(session_uuid: str, msg_in: MessageCreate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Append a user question, update session activity timestamp, and append AI response."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chat_sessions WHERE session_uuid = ? AND user_id = ?;", (session_uuid, current_user["id"]))
    session_row = cursor.fetchone()
    if not session_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")

    session_id = session_row["id"]
    now_str = datetime.now(timezone.utc).isoformat()
    meta_json = json.dumps(msg_in.metadata or {})

    # Insert user message
    cursor.execute("""
        INSERT INTO chat_messages (session_id, sender, content, metadata, created_at)
        VALUES (?, 'user', ?, ?, ?);
    """, (session_id, msg_in.content, meta_json, now_str))
    user_msg_id = cursor.lastrowid

    # Update session title if first question
    cursor.execute("SELECT COUNT(*) FROM chat_messages WHERE session_id = ?;", (session_id,))
    cnt = cursor.fetchone()[0]
    if cnt == 1:
        auto_title = msg_in.content[:40] + ("..." if len(msg_in.content) > 40 else "")
        cursor.execute("UPDATE chat_sessions SET title = ? WHERE id = ?;", (auto_title, session_id))

    # Update last activity
    cursor.execute("UPDATE chat_sessions SET last_activity_at = ? WHERE id = ?;", (now_str, session_id))

    # Simulate AI Assistant Response turn
    ai_reply = f"Thank you for your question regarding '{msg_in.content[:30]}'. I am analyzing your medical profile and query."
    ai_meta = json.dumps({"source": "medical_intelligence_v1", "confidence": 0.95})
    cursor.execute("""
        INSERT INTO chat_messages (session_id, sender, content, metadata, created_at)
        VALUES (?, 'assistant', ?, ?, ?);
    """, (session_id, ai_reply, ai_meta, now_str))

    db.commit()

    cursor.execute("SELECT * FROM chat_messages WHERE id = ?;", (user_msg_id,))
    row = dict(cursor.fetchone())
    row["metadata"] = msg_in.metadata or {}
    return row

@router.delete("/{session_uuid}")
def close_session(session_uuid: str, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Close/delete a consultation chat session."""
    cursor = db.cursor()
    cursor.execute("DELETE FROM chat_sessions WHERE session_uuid = ? AND user_id = ?;", (session_uuid, current_user["id"]))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    db.commit()
    return {"message": "Chat session successfully closed"}
