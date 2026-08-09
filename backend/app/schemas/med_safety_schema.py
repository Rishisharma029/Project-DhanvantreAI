from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class MedicationSafetyRequest(BaseModel):
    medications: List[str] = Field(..., example=["Aspirin", "Warfarin", "Ciprofloxacin"])
    patient_age: Optional[int] = Field(72, description="Patient age in years")
    is_pregnant: bool = Field(False, description="Is patient pregnant")
    trimester: Optional[int] = Field(None, description="Trimester (1, 2, or 3)")
    is_lactating: bool = Field(False, description="Is patient breastfeeding")
    egfr_ml_min: Optional[float] = Field(28.0, description="Estimated GFR in mL/min/1.73m2")
    alt_ast_u_l: Optional[float] = Field(45.0, description="ALT/AST liver enzymes in U/L")
    known_allergies: List[str] = Field(default=["Penicillin"], example=["Penicillin", "Sulfa"])

class SafetyCheckResult(BaseModel):
    check_name: str     # PREGNANCY, LACTATION, PEDIATRICS, GERIATRICS, RENAL, HEPATIC, ALLERGY, QT_PROLONGATION, DUPLICATE_THERAPY, BLACK_BOX_WARNING
    passed: bool
    severity: str       # CRITICAL, HIGH, MODERATE, LOW, NONE
    message: str
    clinical_action: str

class MedicationSafetyResponse(BaseModel):
    safety_score: int                   # 0 to 100
    risk_level: str                     # CRITICAL_RED, HIGH_ORANGE, MODERATE_YELLOW, LOW_GREEN
    total_alerts_found: int
    safety_checks: List[SafetyCheckResult]
    actionable_recommendations: List[str]
    execution_time_ms: int
