import sqlite3
from typing import List, Dict, Any
from app.config import settings
from app.schemas.admin_schema import (
    AdminMedicineCreate, AdminDiseaseCreate, AdminUserRoleUpdate,
    AdminUserItem, AdminReportStatsResponse, AdminDBStatsResponse
)

# 1. MEDICINES ADMIN CRUD
def admin_create_medicine(req: AdminMedicineCreate, db: sqlite3.Connection) -> Dict[str, Any]:
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO medicines (canonical_name, brand_name, generic_name, canonical_key, price_inr, composition)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (req.canonical_name, req.brand_name, req.generic_name, req.canonical_name.lower(), req.price_inr, req.composition))
    db.commit()
    med_id = cursor.lastrowid
    return {"message": "Medicine created successfully", "medicine_id": med_id, "name": req.canonical_name}

def admin_get_medicines(limit: int, db: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = db.cursor()
    cursor.execute("SELECT id, canonical_name, brand_name, generic_name, price_inr FROM medicines ORDER BY id DESC LIMIT ?;", (limit,))
    rows = cursor.fetchall()
    return [{"id": r[0], "canonical_name": r[1], "brand_name": r[2], "generic_name": r[3], "price_inr": r[4]} for r in rows]

def admin_delete_medicine(med_id: int, db: sqlite3.Connection) -> bool:
    cursor = db.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = ?;", (med_id,))
    db.commit()
    return cursor.rowcount > 0

# 2. DISEASES ADMIN CRUD
def admin_create_disease(req: AdminDiseaseCreate, db: sqlite3.Connection) -> Dict[str, Any]:
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO diseases (name, severity_level, description)
        VALUES (?, ?, ?);
    """, (req.name, req.severity_level, req.description))
    disease_id = cursor.lastrowid

    for sym_name in (req.symptoms or []):
        cursor.execute("INSERT OR IGNORE INTO symptoms (name) VALUES (?);", (sym_name.lower(),))
        cursor.execute("SELECT id FROM symptoms WHERE name = ? LIMIT 1;", (sym_name.lower(),))
        sym_id = cursor.fetchone()[0]
        cursor.execute("INSERT OR IGNORE INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?);", (disease_id, sym_id))

    db.commit()
    return {"message": "Disease created successfully", "disease_id": disease_id, "name": req.name}

def admin_get_diseases(limit: int, db: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = db.cursor()
    cursor.execute("SELECT id, name, severity_level, description FROM diseases ORDER BY id DESC LIMIT ?;", (limit,))
    rows = cursor.fetchall()
    return [{"id": r[0], "name": r[1], "severity_level": r[2], "description": r[3]} for r in rows]

def admin_delete_disease(disease_id: int, db: sqlite3.Connection) -> bool:
    cursor = db.cursor()
    cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?;", (disease_id,))
    cursor.execute("DELETE FROM diseases WHERE id = ?;", (disease_id,))
    db.commit()
    return cursor.rowcount > 0

# 3. USERS GOVERNANCE
def admin_get_users(limit: int, db: sqlite3.Connection) -> List[AdminUserItem]:
    cursor = db.cursor()
    cursor.execute("SELECT id, email, full_name, role, is_active, is_verified, created_at FROM users ORDER BY id DESC LIMIT ?;", (limit,))
    rows = cursor.fetchall()
    return [
        AdminUserItem(id=r[0], email=r[1], full_name=r[2], role=r[3], is_active=bool(r[4]), is_verified=bool(r[5]), created_at=str(r[6]))
        for r in rows
    ]

def admin_update_user_role(target_user_id: int, req: AdminUserRoleUpdate, db: sqlite3.Connection) -> AdminUserItem:
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users SET role = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?;
    """, (req.role, 1 if req.is_active else 0, target_user_id))
    db.commit()

    cursor.execute("SELECT id, email, full_name, role, is_active, is_verified, created_at FROM users WHERE id = ?;", (target_user_id,))
    r = cursor.fetchone()
    return AdminUserItem(id=r[0], email=r[1], full_name=r[2], role=r[3], is_active=bool(r[4]), is_verified=bool(r[5]), created_at=str(r[6]))

# 4. REPORTS & AUDIT STATS
def admin_get_report_stats(db: sqlite3.Connection) -> AdminReportStatsResponse:
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    u_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_medical_reports;")
    rep_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_symptom_history;")
    sym_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_medication_history;")
    med_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_followup_visits;")
    fol_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_notifications;")
    notif_cnt = cursor.fetchone()[0]

    return AdminReportStatsResponse(
        total_users=u_cnt,
        total_reports_logged=rep_cnt,
        total_symptoms_logged=sym_cnt,
        total_medications_logged=med_cnt,
        total_followups_scheduled=fol_cnt,
        total_notifications_sent=notif_cnt
    )

# 5. DATABASE MAINTENANCE & HEALTH
def admin_get_db_stats(db: sqlite3.Connection) -> AdminDBStatsResponse:
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [r[0] for r in cursor.fetchall()]

    counts: Dict[str, int] = {}
    for tbl in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
            counts[tbl] = cursor.fetchone()[0]
        except Exception:
            counts[tbl] = 0

    return AdminDBStatsResponse(
        database_path=settings.DATABASE_PATH,
        total_tables=len(tables),
        table_row_counts=counts,
        status="Healthy"
    )

def admin_vacuum_db(db: sqlite3.Connection) -> Dict[str, str]:
    cursor = db.cursor()
    cursor.execute("VACUUM;")
    return {"message": "Database VACUUM maintenance executed successfully", "status": "Optimized"}
