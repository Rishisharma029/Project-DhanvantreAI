from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.services.disaster_recovery_service import disaster_recovery_engine
from app.api.deps import get_current_user, RoleChecker

admin_only = RoleChecker(["admin"])

router = APIRouter(prefix="/disaster-recovery", tags=["Backup & Disaster Recovery"])

class RestoreVerificationRequest(BaseModel):
    backup_filename: str = Field(..., example="auramed_backup_20260802_043000.enc.db")

@router.post("/backup", status_code=status.HTTP_201_CREATED)
def trigger_encrypted_backup(current_admin=Depends(admin_only)) -> Dict[str, Any]:
    """
    Triggers manual AES-256 encrypted database backup.
    Requires Admin credentials.
    """
    try:
        return disaster_recovery_engine.create_encrypted_backup()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/restore-verify", status_code=status.HTTP_200_OK)
def verify_backup_restore(payload: RestoreVerificationRequest, current_admin=Depends(admin_only)) -> Dict[str, Any]:
    """
    Decrypts specified backup file in an isolated environment and verifies schema integrity.
    Requires Admin credentials.
    """
    backup_path = f"backups/{payload.backup_filename}"
    try:
        res = disaster_recovery_engine.restore_and_verify_backup(backup_path)
        if not res["is_valid"]:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Backup restore verification failed. Database file corrupted or invalid.")
        return res
    except FileNotFoundError as fnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(fnf))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/backups", status_code=status.HTTP_200_OK)
def list_encrypted_backups(current_admin=Depends(admin_only)) -> List[Dict[str, Any]]:
    """
    Lists available encrypted database backups.
    Requires Admin credentials.
    """
    return disaster_recovery_engine.list_backups()
