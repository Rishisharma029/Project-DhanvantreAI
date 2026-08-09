from fastapi import APIRouter, status
from typing import Dict, Any
from app.services.performance_service import performance_collector

router = APIRouter(prefix="/performance", tags=["Performance & Telemetry Dashboard"])

@router.get("/stats", status_code=status.HTTP_200_OK)
def get_performance_dashboard_stats() -> Dict[str, Any]:
    """
    Live Performance Dashboard Telemetry API.
    Provides real-time throughput (RPS), memory usage, CPU, request latency (P50/P95/P99), and cache hit rate.
    """
    return performance_collector.get_live_metrics()
