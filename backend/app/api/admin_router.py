import sqlite3
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db
from app.api.auth_router import get_current_user
from app.schemas.admin_schema import (
    AdminMedicineCreate, AdminDiseaseCreate, AdminUserRoleUpdate,
    AdminUserItem, AdminReportStatsResponse, AdminDBStatsResponse
)
from app.services.admin_service import (
    admin_create_medicine, admin_get_medicines, admin_delete_medicine,
    admin_create_disease, admin_get_diseases, admin_delete_disease,
    admin_get_users, admin_update_user_role,
    admin_get_report_stats, admin_get_db_stats, admin_vacuum_db
)

from app.services.audit_service import log_security_audit_event

router = APIRouter(prefix="/admin", tags=["Admin Backend"])

def get_admin_user(current_user = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """RBAC Guard: Enforces Admin role requirement."""
    if current_user.get("role") != "admin":
        log_security_audit_event(
            user_id=current_user.get("id", 0),
            event_type="PERMISSION_DENIED",
            message=f"Access denied to admin route for user: {current_user.get('email')}",
            ip_address="127.0.0.1",
            db=db
        )
        raise HTTPException(status_code=403, detail="Admin authorization required to access this endpoint.")
    return current_user

# 1. MEDICINES ADMIN ENDPOINTS
@router.post("/medicines")
def admin_create_medicine_endpoint(req: AdminMedicineCreate, admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_create_medicine(req, db)

@router.get("/medicines")
def admin_get_medicines_endpoint(limit: int = Query(50, ge=1, le=200), admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_get_medicines(limit, db)

@router.delete("/medicines/{med_id}")
def admin_delete_medicine_endpoint(med_id: int, admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    success = admin_delete_medicine(med_id, db)
    if not success:
        raise HTTPException(status_code=404, detail=f"Medicine ID {med_id} not found.")
    return {"message": f"Medicine ID {med_id} deleted successfully"}

# 2. DISEASES ADMIN ENDPOINTS
@router.post("/diseases")
def admin_create_disease_endpoint(req: AdminDiseaseCreate, admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_create_disease(req, db)

@router.get("/diseases")
def admin_get_diseases_endpoint(limit: int = Query(50, ge=1, le=200), admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_get_diseases(limit, db)

@router.delete("/diseases/{disease_id}")
def admin_delete_disease_endpoint(disease_id: int, admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    success = admin_delete_disease(disease_id, db)
    if not success:
        raise HTTPException(status_code=404, detail=f"Disease ID {disease_id} not found.")
    return {"message": f"Disease ID {disease_id} deleted successfully"}

# 3. USERS GOVERNANCE ENDPOINTS
@router.get("/users", response_model=List[AdminUserItem])
def admin_get_users_endpoint(limit: int = Query(50, ge=1, le=200), admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_get_users(limit, db)

@router.put("/users/{user_id}/role", response_model=AdminUserItem)
def admin_update_user_role_endpoint(user_id: int, req: AdminUserRoleUpdate, admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    res = admin_update_user_role(user_id, req, db)
    log_security_audit_event(
        user_id=admin["id"],
        event_type="ROLE_CHANGED",
        message=f"Admin {admin['email']} updated role of user ID {user_id} to '{req.role}'",
        ip_address="127.0.0.1",
        db=db
    )
    return res


# 4. REPORTS STATS ENDPOINT
@router.get("/reports/stats", response_model=AdminReportStatsResponse)
def admin_get_report_stats_endpoint(admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_get_report_stats(db)

# 5. DB MAINTENANCE ENDPOINTS
@router.get("/db/stats", response_model=AdminDBStatsResponse)
def admin_get_db_stats_endpoint(admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_get_db_stats(db)

@router.post("/db/vacuum")
def admin_vacuum_db_endpoint(admin = Depends(get_admin_user), db: sqlite3.Connection = Depends(get_db)):
    return admin_vacuum_db(db)
