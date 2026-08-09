import sqlite3
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.database import get_db
from app.schemas.medicine_schema import (
    MedicineSearchResponse, MedicineDetailResponse, SubstituteItem
)
from app.services.medicine_retrieval_engine import (
    search_medicines, get_medicine_details, get_medicine_substitutes
)

router = APIRouter(prefix="/medicines", tags=["Medicine Retrieval Engine"])

@router.get("/search", response_model=MedicineSearchResponse)
def search_medicine_endpoint(
    q: str = Query(..., min_length=1, description="Search query term (name, brand, generic, ingredient, use)"),
    by: str = Query("all", description="Search filter mode: all, name, generic, brand, ingredient, use"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db)
):
    """
    Search medicines by Medicine Name, Generic Name, Brand Name, Ingredients, or Uses.
    """
    return search_medicines(query=q, search_by=by, page=page, limit=limit, db=db)

@router.get("/ingredient/{ingredient_name}", response_model=MedicineSearchResponse)
def search_by_ingredient_endpoint(
    ingredient_name: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db)
):
    """Search medicines containing a specific active ingredient."""
    return search_medicines(query=ingredient_name, search_by="ingredient", page=page, limit=limit, db=db)

@router.get("/use/{use_name}", response_model=MedicineSearchResponse)
def search_by_use_endpoint(
    use_name: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db)
):
    """Search medicines indicated for a specific therapeutic use/condition."""
    return search_medicines(query=use_name, search_by="use", page=page, limit=limit, db=db)

@router.get("/{medicine_id}", response_model=MedicineDetailResponse)
def get_medicine_detail_endpoint(medicine_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Fetch complete medicine details by ID (ingredients, manufacturer, side effects, uses, substitutes)."""
    details = get_medicine_details(medicine_id, db)
    if not details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")
    return details

@router.get("/{medicine_id}/substitutes", response_model=list[SubstituteItem])
def get_medicine_substitutes_endpoint(medicine_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Fetch substitute alternative brands for a given medicine ID."""
    details = get_medicine_details(medicine_id, db)
    if not details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")
    return get_medicine_substitutes(medicine_id, db)
