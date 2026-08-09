import sqlite3
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ClinicalFailureEntry(BaseModel):
    failure_id: Optional[str] = None
    failure_type: str = Field(..., description="One of ERR-TRIAGE, ERR-FOLLOWUP, ERR-HALLUC, ERR-REPEAT, ERR-ALLERGY, ERR-INTERACT")
    scenario_description: str
    input_prompt: str
    expected_behavior: str
    actual_behavior: str
    root_cause: str
    fix_applied: str
    status: str = "RESOLVED"

def init_failure_ledger_db(db: sqlite3.Connection):
    """Initializes clinical failure log table in SQLite database."""
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clinical_failure_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            failure_type TEXT NOT NULL,
            scenario_description TEXT NOT NULL,
            input_prompt TEXT NOT NULL,
            expected_behavior TEXT NOT NULL,
            actual_behavior TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            fix_applied TEXT NOT NULL,
            status TEXT DEFAULT 'RESOLVED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()

def log_clinical_failure(entry: ClinicalFailureEntry, db: sqlite3.Connection) -> int:
    """Logs a new clinical failure entry into the failure ledger."""
    init_failure_ledger_db(db)
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO clinical_failure_logs 
        (failure_type, scenario_description, input_prompt, expected_behavior, actual_behavior, root_cause, fix_applied, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        entry.failure_type, entry.scenario_description, entry.input_prompt,
        entry.expected_behavior, entry.actual_behavior, entry.root_cause,
        entry.fix_applied, entry.status
    ))
    db.commit()
    return cursor.lastrowid

def get_all_clinical_failures(db: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Retrieves all logged clinical failures."""
    init_failure_ledger_db(db)
    cursor = db.cursor()
    cursor.execute("SELECT id, failure_type, scenario_description, input_prompt, expected_behavior, actual_behavior, root_cause, fix_applied, status, created_at FROM clinical_failure_logs ORDER BY id DESC;")
    rows = cursor.fetchall()
    return [
        {
            "id": r[0], "failure_type": r[1], "scenario_description": r[2],
            "input_prompt": r[3], "expected_behavior": r[4], "actual_behavior": r[5],
            "root_cause": r[6], "fix_applied": r[7], "status": r[8], "created_at": r[9]
        }
        for r in rows
    ]
