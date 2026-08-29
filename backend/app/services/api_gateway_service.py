import time
import threading
from typing import Dict, List, Tuple, Any
from app.config import settings
from app.schemas.gateway_schema import APIRouteItem, GatewayHealthResponse, RateLimitStatusResponse

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests_log: Dict[str, List[float]] = {}
        self.lock = threading.Lock()

    def check_rate_limit(self, client_ip: str) -> Tuple[bool, int, int]:
        """
        Checks rate limit for client IP.
        Returns (is_allowed, remaining_requests, reset_in_seconds).
        """
        now = time.time()
        window_start = now - self.window_seconds

        with self.lock:
            timestamps = self.requests_log.get(client_ip, [])
            # Filter timestamps outside window
            valid_timestamps = [ts for ts in timestamps if ts > window_start]
            
            if len(valid_timestamps) >= self.max_requests:
                oldest = valid_timestamps[0]
                reset_in = int((oldest + self.window_seconds) - now)
                self.requests_log[client_ip] = valid_timestamps
                return False, 0, max(reset_in, 1)

            valid_timestamps.append(now)
            self.requests_log[client_ip] = valid_timestamps
            remaining = self.max_requests - len(valid_timestamps)
            return True, remaining, self.window_seconds

    def get_status(self, client_ip: str) -> RateLimitStatusResponse:
        now = time.time()
        window_start = now - self.window_seconds
        with self.lock:
            timestamps = [ts for ts in self.requests_log.get(client_ip, []) if ts > window_start]
            used = len(timestamps)
            remaining = max(self.max_requests - used, 0)
            reset_in = 60
            if timestamps:
                reset_in = max(int((timestamps[0] + self.window_seconds) - now), 1)

            return RateLimitStatusResponse(
                client_ip=client_ip,
                max_limit=self.max_requests,
                requests_used=used,
                remaining=remaining,
                reset_in_seconds=reset_in,
                status="ALLOWED" if used < self.max_requests else "EXCEEDED"
            )

# Global Gateway Rate Limiter Instances
gateway_rate_limiter = SlidingWindowRateLimiter(max_requests=100, window_seconds=60)
ai_rate_limiter = SlidingWindowRateLimiter(max_requests=20, window_seconds=60)
password_reset_rate_limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=900)

def get_gateway_health(app) -> GatewayHealthResponse:
    total_routes = len(app.routes)
    return GatewayHealthResponse(
        gateway_status="OPERATIONAL",
        api_version=settings.VERSION,
        total_registered_routes=total_routes,
        rate_limiting_enabled=True,
        rate_limit_max_requests_per_min=100,
        compression_enabled=True,
        min_compression_bytes=500
    )

def get_registered_routes(app) -> List[APIRouteItem]:
    routes: List[APIRouteItem] = []
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            routes.append(APIRouteItem(
                path=route.path,
                name=getattr(route, "name", "route"),
                methods=list(getattr(route, "methods", []))
            ))
    return routes
