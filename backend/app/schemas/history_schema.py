from pydantic import BaseModel, Field
from typing import Optional, List

# 1. Previous Reports Schemas
class MedicalReportCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Report title e.g. 'Complete Blood Count'")
    report_type: str = Field(..., description="Blood Test, Lab Report, Imaging, Clinical Notes")
    report_date: str = Field(..., description="ISO Date YYYY-MM-DD")
    summary_notes: Optional[str] = None

class MedicalReportResponse(BaseModel):
    id: int
    user_id: int
    title: str
    report_type: str
    report_date: str
    summary_notes: Optional[str] = None
    created_at: str

# 2. Previous Symptoms Schemas
class SymptomHistoryCreate(BaseModel):
    symptom_name: str = Field(..., min_length=1, description="Symptom name e.g. 'High Fever'")
    severity: Optional[str] = Field("Moderate", description="Mild, Moderate, Severe")
    onset_date: str = Field(..., description="ISO Date YYYY-MM-DD")
    resolution_date: Optional[str] = None
    notes: Optional[str] = None

class SymptomHistoryResponse(BaseModel):
    id: int
    user_id: int
    symptom_name: str
    severity: str
    onset_date: str
    resolution_date: Optional[str] = None
    notes: Optional[str] = None
    created_at: str

# 3. Previous Medicines Schemas
class MedicationHistoryCreate(BaseModel):
    medicine_name: str = Field(..., min_length=1, description="Medicine name e.g. 'Amoxicillin 500mg'")
    dosage: str = Field(..., description="Dosage e.g. '500mg twice daily'")
    start_date: str = Field(..., description="ISO Date YYYY-MM-DD")
    end_date: Optional[str] = None
    side_effects_noted: Optional[str] = None

class MedicationHistoryResponse(BaseModel):
    id: int
    user_id: int
    medicine_name: str
    dosage: str
    start_date: str
    end_date: Optional[str] = None
    side_effects_noted: Optional[str] = None
    created_at: str

# 4. Follow-up Visits Schemas
class FollowupVisitCreate(BaseModel):
    doctor_name: str = Field(..., min_length=1, description="Doctor or clinic name")
    reason: str = Field(..., description="Consultation reason")
    visit_date: str = Field(..., description="Scheduled visit date YYYY-MM-DD")
    is_completed: Optional[bool] = False
    clinical_notes: Optional[str] = None

class FollowupVisitResponse(BaseModel):
    id: int
    user_id: int
    doctor_name: str
    reason: str
    visit_date: str
    is_completed: bool
    clinical_notes: Optional[str] = None
    created_at: str

# 5. Unified 360 History Summary Schema
class MedicalHistorySummaryResponse(BaseModel):
    user_id: int
    total_reports: int
    reports: List[MedicalReportResponse]
    total_symptoms: int
    symptoms: List[SymptomHistoryResponse]
    total_medicines: int
    medicines: List[MedicationHistoryResponse]
    total_followups: int
    followups: List[FollowupVisitResponse]
