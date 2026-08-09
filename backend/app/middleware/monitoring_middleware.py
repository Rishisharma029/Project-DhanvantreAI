import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.services.monitoring_service import metrics_registry
from app.services.structured_logging_service import StructuredLogger

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        correlation_id = request.headers.get("X-Correlation-ID", f"CORR-{uuid.uuid4().hex[:8].upper()}")
        client_ip = request.client.host if request.client else "127.0.0.1"

        try:
            response = await call_next(request)
            duration_sec = time.time() - start_time
            duration_ms = duration_sec * 1000
            
            endpoint = request.url.path
            metrics_registry.record_http_request(
                method=request.method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration_sec=duration_sec
            )

            # Emit PHI-Safe Structured JSON Log
            StructuredLogger.log_api_request(
                method=request.method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration_ms=duration_ms,
                correlation_id=correlation_id,
                client_ip=client_ip
            )

            response.headers["X-Process-Time"] = f"{duration_sec:.6f}"
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        except Exception as exc:
            duration_sec = time.time() - start_time
            duration_ms = duration_sec * 1000
            metrics_registry.record_http_request(
                method=request.method,
                endpoint=request.url.path,
                status_code=500,
                duration_sec=duration_sec
            )
            StructuredLogger.log_error(
                event_type="UNHANDLED_EXCEPTION",
                error_msg=str(exc),
                correlation_id=correlation_id
            )
            raise exc
