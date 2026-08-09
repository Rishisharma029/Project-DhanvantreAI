import sqlite3
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    UserResponse, ForgotPasswordRequest, ResetPasswordRequest,
    EmailVerifyRequest, GoogleOAuthRequest
)
from app.services.auth_service import (
    hash_password, verify_password, create_access_token,
    generate_random_token, get_refresh_expiry, get_verification_expiry,
    revoke_jti_token
)
from app.services.audit_service import log_security_audit_event
from app.api.deps import get_current_user, RoleChecker, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister, db: sqlite3.Connection = Depends(get_db)):
    """Register a new user account."""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?;", (user_in.email.lower(),))
    if cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    role = user_in.role.lower() if user_in.role and user_in.role.lower() in ("user", "doctor", "admin") else "user"
    hashed_pwd = hash_password(user_in.password)

    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, role, is_active, is_verified)
        VALUES (?, ?, ?, ?, 1, 0);
    """, (user_in.email.lower(), hashed_pwd, user_in.full_name, role))
    user_id = cursor.lastrowid

    # Create verification token
    v_token = generate_random_token()
    v_expiry = get_verification_expiry()
    cursor.execute("""
        INSERT INTO auth_tokens (user_id, token, token_type, expires_at)
        VALUES (?, ?, 'email_verify', ?);
    """, (user_id, v_token, v_expiry))

    db.commit()

    cursor.execute("SELECT id, email, full_name, role, is_active, is_verified, created_at FROM users WHERE id = ?;", (user_id,))
    user_row = cursor.fetchone()
    return dict(user_row)

@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    """Authenticate credentials and issue JWT Access & Refresh Tokens."""
    cursor = db.cursor()
    cursor.execute("SELECT id, email, hashed_password, role, is_active FROM users WHERE email = ?;", (credentials.email.lower(),))
    user = cursor.fetchone()
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        log_security_audit_event(
            user_id=user["id"] if user else 0,
            event_type="LOGIN_FAILED",
            message=f"Failed authentication attempt for email: {credentials.email.lower()}",
            ip_address="127.0.0.1",
            db=db
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user["is_active"]:
        log_security_audit_event(
            user_id=user["id"],
            event_type="ACCOUNT_LOCKED",
            message=f"Attempted login on deactivated account: {credentials.email.lower()}",
            ip_address="127.0.0.1",
            db=db
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")


    access_token = create_access_token(user["id"], user["email"], user["role"])
    refresh_token = generate_random_token()
    r_expiry = get_refresh_expiry()

    cursor.execute("""
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (?, ?, ?);
    """, (user["id"], refresh_token, r_expiry))
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshTokenRequest, db: sqlite3.Connection = Depends(get_db)):
    """Rotate access token using valid refresh token."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT r.id, r.user_id, r.expires_at, r.revoked, u.email, u.role, u.is_active
        FROM refresh_tokens r
        JOIN users u ON r.user_id = u.id
        WHERE r.token = ?;
    """, (body.refresh_token,))
    row = cursor.fetchone()
    
    if not row or row["revoked"] or not row["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or revoked refresh token")

    exp_dt = datetime.fromisoformat(row["expires_at"])
    if exp_dt < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # Issue new tokens and revoke old refresh token
    cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE id = ?;", (row["id"],))
    
    new_access_token = create_access_token(row["user_id"], row["email"], row["role"])
    new_refresh_token = generate_random_token()
    new_r_expiry = get_refresh_expiry()

    cursor.execute("""
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (?, ?, ?);
    """, (row["user_id"], new_refresh_token, new_r_expiry))
    db.commit()

    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

@router.post("/logout")
def logout_user(
    body: RefreshTokenRequest,
    raw_token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Revoke active JWT access token (JTI) and refresh token on logout."""
    cursor = db.cursor()
    
    # Revoke Refresh Token
    cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE token = ? AND user_id = ?;", (body.refresh_token, current_user["id"]))
    
    # Revoke JTI from Access Token
    from app.services.auth_service import decode_access_token
    payload = decode_access_token(raw_token)
    if payload and payload.get("jti"):
        exp_iso = datetime.fromtimestamp(payload.get("exp", 0), timezone.utc).isoformat()
        revoke_jti_token(payload["jti"], current_user["id"], "logout", exp_iso, db)

    log_security_audit_event(
        user_id=current_user["id"],
        event_type="JWT_REVOKED",
        message=f"User {current_user['email']} logged out. Access JTI and Refresh tokens revoked.",
        ip_address="127.0.0.1",
        db=db
    )

    db.commit()
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user

@router.delete("/me")
def delete_my_account(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Right to be Forgotten: Cascading deletion of user account,
    medical profiles, chat sessions, reports, and tokens.
    """
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("DELETE FROM users WHERE id = ?;", (current_user["id"],))

    log_security_audit_event(
        user_id=current_user["id"],
        event_type="ACCOUNT_DELETED",
        message=f"User {current_user['email']} (ID {current_user['id']}) permanently deleted account and associated PHI.",
        ip_address="127.0.0.1",
        db=db
    )

    db.commit()
    return {"message": "Account and all associated personal and medical data have been permanently deleted."}


@router.post("/verify-email")
def verify_email(body: EmailVerifyRequest, db: sqlite3.Connection = Depends(get_db)):
    """Verify user email via token."""
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, expires_at, used FROM auth_tokens WHERE token = ? AND token_type = 'email_verify';", (body.token,))
    row = cursor.fetchone()
    if not row or row["used"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification token")

    cursor.execute("UPDATE users SET is_verified = 1 WHERE id = ?;", (row["user_id"],))
    cursor.execute("UPDATE auth_tokens SET used = 1 WHERE id = ?;", (row["id"],))
    db.commit()
    return {"message": "Email successfully verified"}

@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, db: sqlite3.Connection = Depends(get_db)):
    """Issue password reset token."""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?;", (body.email.lower(),))
    user = cursor.fetchone()
    if not user:
        # Return success to prevent email enumeration
        return {"message": "If account exists, password reset token generated"}

    reset_token = generate_random_token()
    r_expiry = get_verification_expiry()
    cursor.execute("""
        INSERT INTO auth_tokens (user_id, token, token_type, expires_at)
        VALUES (?, ?, 'password_reset', ?);
    """, (user["id"], reset_token, r_expiry))
    db.commit()

    return {"message": "Password reset token generated", "reset_token": reset_token}

@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, db: sqlite3.Connection = Depends(get_db)):
    """Reset password using valid token and revoke all previous sessions."""
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, expires_at, used FROM auth_tokens WHERE token = ? AND token_type = 'password_reset';", (body.token,))
    row = cursor.fetchone()
    if not row or row["used"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    new_hash = hash_password(body.new_password)
    cursor.execute("UPDATE users SET hashed_password = ? WHERE id = ?;", (new_hash, row["user_id"]))
    cursor.execute("UPDATE auth_tokens SET used = 1 WHERE id = ?;", (row["id"],))
    
    # Revoke all active refresh tokens on password reset for security
    cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE user_id = ?;", (row["user_id"],))

    log_security_audit_event(
        user_id=row["user_id"],
        event_type="PASSWORD_CHANGED",
        message=f"Password successfully reset for user ID: {row['user_id']}. Active sessions revoked.",
        ip_address="127.0.0.1",
        db=db
    )

    db.commit()
    return {"message": "Password successfully updated"}


@router.post("/google", response_model=TokenResponse)
def google_oauth(body: GoogleOAuthRequest, db: sqlite3.Connection = Depends(get_db)):
    """Authenticate or provision user via Google OAuth ID token."""
    # Mock/simulated Google ID token verification for test/demo mode
    mock_google_email = f"user_{hash(body.id_token) % 10000}@gmail.com"
    mock_google_name = "Google OAuth User"

    cursor = db.cursor()
    cursor.execute("SELECT id, email, role, is_active FROM users WHERE email = ?;", (mock_google_email,))
    user = cursor.fetchone()

    if not user:
        random_pwd = hash_password(generate_random_token())
        cursor.execute("""
            INSERT INTO users (email, hashed_password, full_name, role, is_active, is_verified)
            VALUES (?, ?, ?, 'user', 1, 1);
        """, (mock_google_email, random_pwd, mock_google_name))
        db.commit()
        user_id = cursor.lastrowid
        user_role = "user"
    else:
        user_id = user["id"]
        user_role = user["role"]

    access_token = create_access_token(user_id, mock_google_email, user_role)
    refresh_token = generate_random_token()
    r_expiry = get_refresh_expiry()

    cursor.execute("INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (?, ?, ?);", (user_id, refresh_token, r_expiry))
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

# RBAC Protected Routes
@router.get("/admin-only", dependencies=[Depends(RoleChecker(["admin"]))])
def admin_only_route():
    return {"status": "success", "message": "Welcome Admin! Access granted."}

@router.get("/doctor-only", dependencies=[Depends(RoleChecker(["doctor", "admin"]))])
def doctor_only_route():
    return {"status": "success", "message": "Welcome Doctor! Access granted."}
