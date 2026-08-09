from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class APIRouteItem(BaseModel):
    path: str
    name: str
    methods: List[str]

class GatewayHealthResponse(BaseModel):
    gateway_status: str
    api_version: str
    total_registered_routes: int
    rate_limiting_enabled: bool
    rate_limit_max_requests_per_min: int
    compression_enabled: bool
    min_compression_bytes: int

class RateLimitStatusResponse(BaseModel):
    client_ip: str
    max_limit: int
    requests_used: int
    remaining: int
    reset_in_seconds: int
    status: str
