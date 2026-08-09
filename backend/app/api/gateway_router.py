from fastapi import APIRouter, Request
from app.schemas.gateway_schema import GatewayHealthResponse, APIRouteItem, RateLimitStatusResponse
from app.services.api_gateway_service import (
    gateway_rate_limiter, get_gateway_health, get_registered_routes
)

router = APIRouter(prefix="/gateway", tags=["API Gateway"])

@router.get("/health", response_model=GatewayHealthResponse)
def get_gateway_health_endpoint(request: Request):
    """Retrieve API Gateway operational status, registered route count, and compression configuration."""
    return get_gateway_health(request.app)

@router.get("/routes", response_model=list[APIRouteItem])
def get_gateway_routes_endpoint(request: Request):
    """Retrieve all central API Gateway registered routes and HTTP methods."""
    return get_registered_routes(request.app)

@router.get("/rate-limit-status", response_model=RateLimitStatusResponse)
def get_rate_limit_status_endpoint(request: Request):
    """Check current client IP rate limit consumption and remaining quota."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    return gateway_rate_limiter.get_status(client_ip)
