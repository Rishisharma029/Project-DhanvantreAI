from pydantic import BaseModel, Field
from typing import Optional, List

class DosageReferenceResponse(BaseModel):
    medicine_name: str
    generic_name: Optional[str] = None
    composition: Optional[str] = None
    standard_adult_dose: str
    pediatric_dose: str
    maximum_daily_dose: str
    route: str # Oral, Intravenous, Topical, Ophthalmic, etc.
    frequency: str # Every 6-8 hours, Once daily (QD), Twice daily (BID), Three times daily (TID)
    duration: str # 5-7 days, 7-10 days, As needed (PRN)
    disclaimer: str = "Reference information only, not personalized prescribing. Always consult a licensed physician or pharmacist before taking any medication."
