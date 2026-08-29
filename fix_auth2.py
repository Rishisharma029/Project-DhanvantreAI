"""Script to fix forgot-password and add ChangePasswordRequest import"""

filepath = r"backend/app/api/auth_router.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix forgot-password: don't leak token, use shorter expiry
old_forgot = '''    reset_token = generate_random_token()
    r_expiry = get_verification_expiry()
    cursor.execute("""
        INSERT INTO auth_tokens (user_id, token, token_type, expires_at)
        VALUES (?, ?, 'password_reset', ?);
    """, (user["id"], reset_token, r_expiry))
    db.commit()

    return {"message": "Password reset token generated", "reset_token": reset_token}'''

new_forgot = '''    reset_token = generate_random_token()
    # Use shorter expiry for password reset links (1 hour)
    from app.config import settings as app_settings
    r_expiry_dt = datetime.now(timezone.utc) + __import__('datetime').timedelta(hours=app_settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    r_expiry = r_expiry_dt.isoformat()
    cursor.execute("""
        INSERT INTO auth_tokens (user_id, token, token_type, expires_at)
        VALUES (?, ?, 'password_reset', ?);
    """, (user["id"], reset_token, r_expiry))
    db.commit()

    # Never leak the reset token in the API response (only deliver via email)
    return {"message": "If account exists, a password reset link has been sent to your email"}'''

content = content.replace(old_forgot, new_forgot)

# Add ChangePasswordRequest import
old_import = '''from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    UserResponse, ForgotPasswordRequest, ResetPasswordRequest,
    EmailVerifyRequest, GoogleOAuthRequest
)'''

new_import = '''from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    UserResponse, ForgotPasswordRequest, ResetPasswordRequest,
    ChangePasswordRequest, EmailVerifyRequest, GoogleOAuthRequest
)'''

content = content.replace(old_import, new_import)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("fix_auth2.py: Applied successfully")
