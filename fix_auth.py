"""Script to apply security fixes to auth_router.py"""

filepath = r"backend/app/api/auth_router.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Add expiry check to reset-password
old_text1 = '''    if not row or row["used"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    new_hash = hash_password(body.new_password)'''

new_text1 = '''    if not row or row["used"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    # Enforce reset link expiry check
    try:
        exp_dt = datetime.fromisoformat(row["expires_at"])
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        if exp_dt < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset link has expired. Please request a new one.")
    except HTTPException:
        raise
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    new_hash = hash_password(body.new_password)'''

content = content.replace(old_text1, new_text1)

# Fix 2: Add password_changed_at and full session revocation
old_text2 = '''    cursor.execute("UPDATE auth_tokens SET used = 1 WHERE id = ?;", (row["id"],))
    
    # Revoke all active refresh tokens on password reset for security
    cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE user_id = ?;", (row["user_id"],))'''

new_text2 = '''    cursor.execute("UPDATE auth_tokens SET used = 1 WHERE id = ?;", (row["id"],))

    # Revoke ALL active sessions on password reset:
    # 1. Set password_changed_at for JWT session invalidation
    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("UPDATE users SET password_changed_at = ? WHERE id = ?;", (now_str, row["user_id"]))
    # 2. Revoke all refresh tokens
    cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE user_id = ?;", (row["user_id"],))
    # 3. Revoke all active JWT access tokens (JTIs) for this user
    cursor.execute("SELECT jti, expires_at FROM revoked_jwt_tokens WHERE user_id = ?;", (row["user_id"],))'''

content = content.replace(old_text2, new_text2)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("auth_router.py updated successfully")

# Now add the change-password endpoint
old_text3 = '''@router.post("/google", response_model=TokenResponse)'''

new_text3 = '''@router.post("/change-password")
def change_password(
    body: ChangePasswordRequest,
    raw_token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """
    Change password for authenticated user.
    Revokes ALL sessions (JWT + refresh tokens) and sets password_changed_at.
    """
    cursor = db.cursor()
    
    # Verify current password
    cursor.execute("SELECT hashed_password FROM users WHERE id = ?;", (current_user["id"],))
    user_row = cursor.fetchone()
    if not user_row or not verify_password(body.current_password, user_row["hashed_password"]):
        log_security_audit_event(
            user_id=current_user["id"],
            event_type="PASSWORD_CHANGE_FAILED",
            message=f"Failed password change attempt for user: {current_user['email']}",
            ip_address="127.0.0.1",
            db=db
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    # Update password
    new_hash = hash_password(body.new_password)
    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("UPDATE users SET hashed_password = ? WHERE id = ?;", (new_hash, current_user["id"]))
    # Set password_changed_at to invalidate all existing JWT access tokens
    cursor.execute("UPDATE users SET password_changed_at = ? WHERE id = ?;", (now_str, current_user["id"]))

    # Revoke all refresh tokens
    cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE user_id = ?;", (current_user["id"],))

    # Revoke the current JWT (JTI)
    from app.services.auth_service import decode_access_token, revoke_jti_token
    payload = decode_access_token(raw_token)
    if payload and payload.get("jti"):
        exp_iso = datetime.fromtimestamp(payload.get("exp", 0), timezone.utc).isoformat()
        revoke_jti_token(payload["jti"], current_user["id"], "password_change", exp_iso, db)

    log_security_audit_event(
        user_id=current_user["id"],
        event_type="PASSWORD_CHANGED",
        message=f"Password changed for user {current_user['email']}. All sessions revoked.",
        ip_address="127.0.0.1",
        db=db
    )

    db.commit()
    return {"message": "Password successfully changed. All sessions have been terminated. Please log in again."}


@router.post("/google", response_model=TokenResponse)'''

content = content.replace(old_text3, new_text3)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("change-password endpoint added")
