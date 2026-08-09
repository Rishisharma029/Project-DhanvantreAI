from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SearchResultItem(BaseModel):
    id: int
    category: str # Medicine, Disease, Symptom, Ingredient, Manufacturer
    title: str
    subtitle: Optional[str] = None
    description_snippet: Optional[str] = None
    relevance_score: float = 1.0
    metadata: Optional[Dict[str, Any]] = {}

class UniversalSearchResponse(BaseModel):
    query: str
    domain_filter: str
    total_results: int
    categories_found: List[str]
    results_by_category: Dict[str, List[SearchResultItem]]
    all_results: List[SearchResultItem]
