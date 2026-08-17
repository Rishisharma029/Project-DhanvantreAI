"""
CSRF (Cross-Site Request Forgery) Protection Middleware

Implements the Double Submit Cookie pattern for CSRF protection.
- Safe methods (GET, HEAD, OPTIONS) are exempt.
- Unsafe methods (POST, PUT, DELETE, PATCH) require a valid CSRF token
  that matches the CSRF cookie.
- Can be toggled via CSRF_ENABLED environment variable.
"""

import os
import secrets
from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Constants
CSRF_COOKIE_NAME = "XSRF-TOKEN"
CSRF_HEADER_NAME = "X-XSRF-TOKEN"
CSRF_TOKEN_LENGTH = 64  # 32 bytes hex = 64 chars
# Exempt paths (e.g., health checks)
EXEMPT_PATHS = ["/health", "/live", "/ready", "/api/v1/docs", "/api/v1/openapi.json", "/api/v1/auth/csrf-token"]
# Paths that don't need CSRF (API-only with Bearer token auth)
CSRF_BYPASS_PATHS = ["/api/v1/auth/login", "/api/v1/auth/register"]


def is_csrf_enabled() -> bool:
    """Check if CSRF protection should be enforced."""
    return os.environ.get("CSRF_ENABLED", "false").lower() in ("true", "1", "yes")


class CSRFMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce CSRF protection using the Double Submit Cookie pattern."""

    def __init__(self, app, secret_key: Optional[str] = None):
        super().__init__(app)
        self.secret_key = secret_key or os.environ.get("SECRET_KEY", secrets.token_hex(32))

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Always allow exempt paths
        if any(path.startswith(exempt) for exempt in EXEMPT_PATHS):
            return await call_next(request)

        # CSRF bypass paths (auth endpoints protected by other mechanisms)
        if any(path.startswith(bypass) for bypass in CSRF_BYPASS_PATHS):
            return await call_next(request)

        # Safe methods are always exempt
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return await call_next(request)

        # Only enforce if CSRF_ENABLED is set
        if not is_csrf_enabled():
            return await call_next(request)

        # When CSRF is enabled, enforce the double-submit cookie pattern
        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)

        if not csrf_cookie:
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF token missing. Please refresh and try again."}
            )

        csrf_header = request.headers.get(CSRF_HEADER_NAME)

        if not csrf_header:
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF token missing in request header."}
            )

        if not self._validate_token(csrf_cookie, csrf_header):
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF token mismatch. Please refresh and try again."}
            )

        response = await call_next(request)
        return response

    def _validate_token(self, cookie_token: str, header_token: str) -> bool:
        """
        Validates the token using constant-time comparison.
        In Double Submit Cookie pattern, the cookie and header should match exactly.
        """
        if len(cookie_token) != CSRF_TOKEN_LENGTH:
            return False

        import hmac
        return hmac.compare_digest(cookie_token, header_token)

    @staticmethod
    def generate_csrf_token() -> str:
        """Generate a new CSRF token."""
        return secrets.token_hex(32)
