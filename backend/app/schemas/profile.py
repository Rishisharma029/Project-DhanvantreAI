import json
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class MedicalProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = "Prefer not to say"
    height_cm: Optional[float] = Field(None, ge=30.0, le=250.0)
    weight_kg: Optional[float] = Field(None, ge=2.0, le=300.0)
    blood_group: Optional[str] = "Unknown"
    pregnancy_status: Optional[bool] = False
    allergies: Optional[List[str]] = []
    chronic_diseases: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []
    past_medical_history: Optional[str] = ""
    family_history: Optional[str] = ""
    smoking_status: Optional[str] = "Non-Smoker" # Non-Smoker, Occasional, Regular, Former
    alcohol_consumption: Optional[str] = "None" # None, Occasional, Moderate, Heavy

class MedicalProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    gender: Optional[str] = "Prefer not to say"
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    blood_group: Optional[str] = "Unknown"
    pregnancy_status: bool = False
    allergies: List[str] = []
    chronic_diseases: List[str] = []
    current_medications: List[str] = []
    past_medical_history: Optional[str] = ""
    family_history: Optional[str] = ""
    smoking_status: Optional[str] = "Non-Smoker"
    alcohol_consumption: Optional[str] = "None"
    updated_at: str

    @classmethod
    def from_db_row(cls, row: dict):
        """Helper to parse database JSON strings into Python lists."""
        d = dict(row)
        for field in ['allergies', 'chronic_diseases', 'current_medications']:
            if isinstance(d.get(field), str):
                try:
                    d[field] = json.loads(d[field])
                except Exception:
                    d[field] = []
        d['pregnancy_status'] = bool(d.get('pregnancy_status'))
        return cls(**d)
