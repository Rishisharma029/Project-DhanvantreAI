from pydantic import BaseModel, Field
from typing import Optional, List

class IngredientItem(BaseModel):
    ingredient_name: str
    strength: Optional[float] = None
    unit: Optional[str] = ""

class SubstituteItem(BaseModel):
    substitute_medicine_id: Optional[int] = None
    substitute_name: str
    price_inr: Optional[float] = None
    manufacturer_name: Optional[str] = ""

class MedicineSummary(BaseModel):
    id: int
    canonical_name: str
    brand_name: str
    generic_name: Optional[str] = None
    price_inr: Optional[float] = None
    is_discontinued: bool = False
    pack_size_label: Optional[str] = None
    composition: Optional[str] = None
    type: Optional[str] = "allopathy"
    manufacturer_name: Optional[str] = None

class MedicineDetailResponse(MedicineSummary):
    pregnancy_category: Optional[str] = None
    alcohol_warning: Optional[str] = None
    csa_schedule: Optional[str] = None
    rx_otc: Optional[str] = None
    ingredients: List[IngredientItem] = []
    aliases: List[str] = []
    side_effects: List[str] = []
    uses: List[str] = []
    substitutes: List[SubstituteItem] = []

class MedicineSearchResponse(BaseModel):
    query: str
    search_by: str
    page: int
    limit: int
    total_results: int
    medicines: List[MedicineSummary]
