import sqlite3
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.services.auth_service import decode_access_token, is_jti_revoked
from datetime import datetime, timezone
from app.schemas.auth import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: sqlite3.Connection = Depends(get_db)) -> dict:
    """Dependency to retrieve authenticated current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    jti = payload.get("jti")
    if jti and is_jti_revoked(jti, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception


    # Enforce session invalidation on password change:
    # If the JWT was issued (iat) before the password was last changed, reject it
    pwd_changed_at = payload.get("password_changed_at")
    token_iat = payload.get("iat")
    if pwd_changed_at and token_iat:
        pwd_changed_dt = datetime.fromisoformat(pwd_changed_at)
        if pwd_changed_dt.tzinfo is None:
            pwd_changed_dt = pwd_changed_dt.replace(tzinfo=timezone.utc)
        iat_dt = datetime.fromtimestamp(token_iat, tz=timezone.utc)
        if iat_dt < pwd_changed_dt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session invalidated due to password change. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    cursor = db.cursor()
    cursor.execute("SELECT id, email, full_name, role, is_active, is_verified, created_at, password_changed_at FROM users WHERE id = ?;", (user_id,))
    row = cursor.fetchone()
    if not row:
        raise credentials_exception

    user_dict = dict(row)
    if not user_dict.get("is_active"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

    # Cross-check DB: if password_changed_at is newer than the token's iat, reject
    db_pwd_changed = user_dict.get("password_changed_at")
    if db_pwd_changed and token_iat:
        pwd_changed_dt = datetime.fromisoformat(db_pwd_changed)
        if pwd_changed_dt.tzinfo is None:
            pwd_changed_dt = pwd_changed_dt.replace(tzinfo=timezone.utc)
        iat_dt = datetime.fromtimestamp(token_iat, tz=timezone.utc)
        if iat_dt < pwd_changed_dt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session invalidated due to password change. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return user_dict

class RoleChecker:
    """Dependency class to enforce Role-Based Access Control (RBAC)."""
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of the following roles: {self.allowed_roles}"
            )
        return current_user
