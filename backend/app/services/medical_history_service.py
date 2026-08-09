import sqlite3
from typing import List
from app.schemas.history_schema import (
    MedicalReportCreate, MedicalReportResponse,
    SymptomHistoryCreate, SymptomHistoryResponse,
    MedicationHistoryCreate, MedicationHistoryResponse,
    FollowupVisitCreate, FollowupVisitResponse,
    MedicalHistorySummaryResponse
)

# 1. REPORTS SERVICE
def create_user_report(user_id: int, req: MedicalReportCreate, db: sqlite3.Connection) -> MedicalReportResponse:
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO user_medical_reports (user_id, title, report_type, report_date, summary_notes)
        VALUES (?, ?, ?, ?, ?);
    """, (user_id, req.title, req.report_type, req.report_date, req.summary_notes))
    db.commit()
    report_id = cursor.lastrowid
    
    cursor.execute("SELECT id, user_id, title, report_type, report_date, summary_notes, created_at FROM user_medical_reports WHERE id = ?;", (report_id,))
    row = cursor.fetchone()
    return MedicalReportResponse(
        id=row[0], user_id=row[1], title=row[2], report_type=row[3], report_date=row[4], summary_notes=row[5], created_at=str(row[6])
    )

def get_user_reports(user_id: int, db: sqlite3.Connection) -> List[MedicalReportResponse]:
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, title, report_type, report_date, summary_notes, created_at FROM user_medical_reports WHERE user_id = ? ORDER BY report_date DESC;", (user_id,))
    rows = cursor.fetchall()
    return [
        MedicalReportResponse(id=r[0], user_id=r[1], title=r[2], report_type=r[3], report_date=r[4], summary_notes=r[5], created_at=str(r[6]))
        for r in rows
    ]

# 2. SYMPTOMS SERVICE
def create_symptom_history(user_id: int, req: SymptomHistoryCreate, db: sqlite3.Connection) -> SymptomHistoryResponse:
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO user_symptom_history (user_id, symptom_name, severity, onset_date, resolution_date, notes)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (user_id, req.symptom_name, req.severity, req.onset_date, req.resolution_date, req.notes))
    db.commit()
    sym_id = cursor.lastrowid
    
    cursor.execute("SELECT id, user_id, symptom_name, severity, onset_date, resolution_date, notes, created_at FROM user_symptom_history WHERE id = ?;", (sym_id,))
    row = cursor.fetchone()
    return SymptomHistoryResponse(
        id=row[0], user_id=row[1], symptom_name=row[2], severity=row[3], onset_date=row[4], resolution_date=row[5], notes=row[6], created_at=str(row[7])
    )

def get_symptom_history(user_id: int, db: sqlite3.Connection) -> List[SymptomHistoryResponse]:
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, symptom_name, severity, onset_date, resolution_date, notes, created_at FROM user_symptom_history WHERE user_id = ? ORDER BY onset_date DESC;", (user_id,))
    rows = cursor.fetchall()
    return [
        SymptomHistoryResponse(id=r[0], user_id=r[1], symptom_name=r[2], severity=r[3], onset_date=r[4], resolution_date=r[5], notes=r[6], created_at=str(r[7]))
        for r in rows
    ]

# 3. MEDICINES SERVICE
def create_medication_history(user_id: int, req: MedicationHistoryCreate, db: sqlite3.Connection) -> MedicationHistoryResponse:
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO user_medication_history (user_id, medicine_name, dosage, start_date, end_date, side_effects_noted)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (user_id, req.medicine_name, req.dosage, req.start_date, req.end_date, req.side_effects_noted))
    db.commit()
    med_id = cursor.lastrowid
    
    cursor.execute("SELECT id, user_id, medicine_name, dosage, start_date, end_date, side_effects_noted, created_at FROM user_medication_history WHERE id = ?;", (med_id,))
    row = cursor.fetchone()
    return MedicationHistoryResponse(
        id=row[0], user_id=row[1], medicine_name=row[2], dosage=row[3], start_date=row[4], end_date=row[5], side_effects_noted=row[6], created_at=str(row[7])
    )

def get_medication_history(user_id: int, db: sqlite3.Connection) -> List[MedicationHistoryResponse]:
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, medicine_name, dosage, start_date, end_date, side_effects_noted, created_at FROM user_medication_history WHERE user_id = ? ORDER BY start_date DESC;", (user_id,))
    rows = cursor.fetchall()
    return [
        MedicationHistoryResponse(id=r[0], user_id=r[1], medicine_name=r[2], dosage=r[3], start_date=r[4], end_date=r[5], side_effects_noted=r[6], created_at=str(r[7]))
        for r in rows
    ]

# 4. FOLLOWUP VISITS SERVICE
def create_followup_visit(user_id: int, req: FollowupVisitCreate, db: sqlite3.Connection) -> FollowupVisitResponse:
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO user_followup_visits (user_id, doctor_name, reason, visit_date, is_completed, clinical_notes)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (user_id, req.doctor_name, req.reason, req.visit_date, 1 if req.is_completed else 0, req.clinical_notes))
    db.commit()
    visit_id = cursor.lastrowid
    
    cursor.execute("SELECT id, user_id, doctor_name, reason, visit_date, is_completed, clinical_notes, created_at FROM user_followup_visits WHERE id = ?;", (visit_id,))
    row = cursor.fetchone()
    return FollowupVisitResponse(
        id=row[0], user_id=row[1], doctor_name=row[2], reason=row[3], visit_date=row[4], is_completed=bool(row[5]), clinical_notes=row[6], created_at=str(row[7])
    )

def get_followup_visits(user_id: int, db: sqlite3.Connection) -> List[FollowupVisitResponse]:
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, doctor_name, reason, visit_date, is_completed, clinical_notes, created_at FROM user_followup_visits WHERE user_id = ? ORDER BY visit_date DESC;", (user_id,))
    rows = cursor.fetchall()
    return [
        FollowupVisitResponse(id=r[0], user_id=r[1], doctor_name=r[2], reason=r[3], visit_date=r[4], is_completed=bool(r[5]), clinical_notes=r[6], created_at=str(r[7]))
        for r in rows
    ]

# 5. UNIFIED 360 SUMMARY SERVICE
def get_user_medical_history_summary(user_id: int, db: sqlite3.Connection) -> MedicalHistorySummaryResponse:
    reports = get_user_reports(user_id, db)
    symptoms = get_symptom_history(user_id, db)
    medicines = get_medication_history(user_id, db)
    followups = get_followup_visits(user_id, db)

    return MedicalHistorySummaryResponse(
        user_id=user_id,
        total_reports=len(reports),
        reports=reports,
        total_symptoms=len(symptoms),
        symptoms=symptoms,
        total_medicines=len(medicines),
        medicines=medicines,
        total_followups=len(followups),
        followups=followups
    )
