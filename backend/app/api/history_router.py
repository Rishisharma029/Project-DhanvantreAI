import sqlite3
from typing import List
from fastapi import APIRouter, Depends
from app.database import get_db
from app.api.auth_router import get_current_user
from app.schemas.history_schema import (
    MedicalReportCreate, MedicalReportResponse,
    SymptomHistoryCreate, SymptomHistoryResponse,
    MedicationHistoryCreate, MedicationHistoryResponse,
    FollowupVisitCreate, FollowupVisitResponse,
    MedicalHistorySummaryResponse
)
from app.services.medical_history_service import (
    create_user_report, get_user_reports,
    create_symptom_history, get_symptom_history,
    create_medication_history, get_medication_history,
    create_followup_visit, get_followup_visits,
    get_user_medical_history_summary
)

router = APIRouter(prefix="/history", tags=["Medical History Service"])

# 1. REPORTS ENDPOINTS
@router.post("/reports", response_model=MedicalReportResponse)
def add_report_endpoint(req: MedicalReportCreate, current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Log a previous medical/lab report for the authenticated user."""
    return create_user_report(current_user["id"], req, db)

@router.get("/reports", response_model=List[MedicalReportResponse])
def get_reports_endpoint(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve all logged medical reports for the authenticated user."""
    return get_user_reports(current_user["id"], db)

# 2. SYMPTOMS ENDPOINTS
@router.post("/symptoms", response_model=SymptomHistoryResponse)
def add_symptom_endpoint(req: SymptomHistoryCreate, current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Log a historical symptom episode for the authenticated user."""
    return create_symptom_history(current_user["id"], req, db)

@router.get("/symptoms", response_model=List[SymptomHistoryResponse])
def get_symptoms_endpoint(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve all historical symptom episodes for the authenticated user."""
    return get_symptom_history(current_user["id"], db)

# 3. MEDICINES ENDPOINTS
@router.post("/medicines", response_model=MedicationHistoryResponse)
def add_medicine_endpoint(req: MedicationHistoryCreate, current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Log a past medication record for the authenticated user."""
    return create_medication_history(current_user["id"], req, db)

@router.get("/medicines", response_model=List[MedicationHistoryResponse])
def get_medicines_endpoint(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve all past medication records for the authenticated user."""
    return get_medication_history(current_user["id"], db)

# 4. FOLLOWUP VISITS ENDPOINTS
@router.post("/followups", response_model=FollowupVisitResponse)
def add_followup_endpoint(req: FollowupVisitCreate, current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Schedule or record a follow-up visit for the authenticated user."""
    return create_followup_visit(current_user["id"], req, db)

@router.get("/followups", response_model=List[FollowupVisitResponse])
def get_followups_endpoint(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve all follow-up visits for the authenticated user."""
    return get_followup_visits(current_user["id"], db)

# 5. UNIFIED 360 SUMMARY ENDPOINT
@router.get("/summary", response_model=MedicalHistorySummaryResponse)
def get_summary_endpoint(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Retrieve unified 360° medical history timeline summary covering Reports, Symptoms, Medicines, and Follow-up Visits."""
    return get_user_medical_history_summary(current_user["id"], db)
