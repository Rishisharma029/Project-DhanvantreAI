from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AdminMedicineCreate(BaseModel):
    canonical_name: str = Field(..., min_length=1, description="Canonical medicine name")
    brand_name: str = Field(..., description="Brand name")
    generic_name: str = Field(..., description="Generic active name")
    composition: Optional[str] = None
    price_inr: Optional[float] = 0.0

class AdminDiseaseCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Disease name")
    severity_level: str = Field("Moderate", description="Emergency, Severe, Moderate, Mild")
    description: Optional[str] = None
    symptoms: Optional[List[str]] = []

class AdminUserRoleUpdate(BaseModel):
    role: str = Field(..., description="user, doctor, admin")
    is_active: Optional[bool] = True

class AdminUserItem(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: str

class AdminReportStatsResponse(BaseModel):
    total_users: int
    total_reports_logged: int
    total_symptoms_logged: int
    total_medications_logged: int
    total_followups_scheduled: int
    total_notifications_sent: int

class AdminDBStatsResponse(BaseModel):
    database_path: str
    total_tables: int
    table_row_counts: Dict[str, int]
    status: str
