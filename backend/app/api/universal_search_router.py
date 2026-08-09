import sqlite3
from fastapi import APIRouter, Depends, Query
from app.database import get_db
from app.schemas.universal_search_schema import UniversalSearchResponse
from app.services.search_api_service import execute_universal_search

router = APIRouter(prefix="/search", tags=["Search API Service (Universal Search)"])

@router.get("/universal", response_model=UniversalSearchResponse)
def universal_search_endpoint(
    q: str = Query(..., min_length=1, description="Search query string"),
    domain: str = Query("all", description="Domain filter: all, medicines, diseases, symptoms, ingredients, manufacturers"),
    limit: int = Query(20, ge=1, le=100, description="Max results per domain"),
    db: sqlite3.Connection = Depends(get_db)
):
    """
    Execute Universal Search across 5 Clinical Domains:
    - Medicines
    - Diseases
    - Symptoms
    - Ingredients
    - Manufacturers
    """
    return execute_universal_search(q, domain, limit, db)
