import secrets
import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from app.config import settings

def hash_password(password: str) -> str:
    """Hash password using bcrypt directly."""
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against bcrypt hash string."""
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

def create_access_token(user_id: int, email: str, role: str, password_changed_at: str = None) -> str:
    """Create short-lived JWT access token with unique JTI and IAT.
    
    Includes password_changed_at in the payload so the auth dependency
    can reject tokens issued before a password change.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "type": "access"
    }
    if password_changed_at:
        payload["password_changed_at"] = password_changed_at
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Decode and validate JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except jwt.PyJWTError:
        return None

def generate_random_token() -> str:
    """Generate secure random hex token."""
    return secrets.token_hex(32)

def get_refresh_expiry() -> str:
    """Get ISO string format for refresh token expiration."""
    exp = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return exp.isoformat()

def get_verification_expiry() -> str:
    """Get ISO string format for verification/reset token expiration."""
    exp = datetime.now(timezone.utc) + timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRE_HOURS)
    return exp.isoformat()

def revoke_jti_token(jti: str, user_id: int, reason: str, expires_at: str, db) -> bool:
    """Add a JWT JTI to the revocation list (logout, password reset, compromised account)."""
    if not jti:
        return False
    cursor = db.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO revoked_jwt_tokens (jti, user_id, reason, expires_at)
        VALUES (?, ?, ?, ?);
    """, (jti, user_id, reason, expires_at))
    db.commit()
    return True

def is_jti_revoked(jti: str, db) -> bool:
    """Check if JWT JTI has been revoked prior to token expiration."""
    if not jti:
        return False
    cursor = db.cursor()
    cursor.execute("SELECT id FROM revoked_jwt_tokens WHERE jti = ?;", (jti,))
    return cursor.fetchone() is not None

