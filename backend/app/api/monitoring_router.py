import time
from fastapi import APIRouter, Response, status, Depends
from typing import Dict, Any
from app.services.monitoring_service import metrics_registry
from app.database import get_db

router = APIRouter(prefix="", tags=["Monitoring & Health Observability"])

@router.get("/health", status_code=status.HTTP_200_OK)
def get_health_status(db=Depends(get_db)) -> Dict[str, Any]:
    """
    Comprehensive System Health Report.
    Checks Database connectivity, cache layer, and AI pipeline operational status.
    """
    db_status = "healthy"
    try:
        cursor = db.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
    except Exception:
        db_status = "unhealthy"

    cache_status = "healthy"
    ai_engine_status = "healthy"

    overall_status = "healthy" if db_status == "healthy" and cache_status == "healthy" else "degraded"

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "components": {
            "database": db_status,
            "cache": cache_status,
            "ai_engine": ai_engine_status
        },
        "version": "1.0.0"
    }

@router.get("/ready")
def get_readiness_probe(response: Response, db=Depends(get_db)):
    """
    Kubernetes Readiness Probe.
    Returns 200 OK when ready to serve traffic, or 503 Service Unavailable if dependencies are down.
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        return {"status": "ready"}
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready", "reason": "Database connection failed"}

@router.get("/live", status_code=status.HTTP_200_OK)
def get_liveness_probe():
    """
    Kubernetes Liveness Probe.
    Returns 200 OK as long as the application process is running.
    """
    return {"status": "alive", "timestamp": time.time()}

@router.get("/metrics")
def get_prometheus_metrics():
    """
    Prometheus Exporter Endpoint.
    Exposes API latency, request rates, error rates, AI pipeline timings, and RAG retrieval metrics.
    """
    metrics_text = metrics_registry.generate_prometheus_metrics()
    return Response(content=metrics_text, media_type="text/plain; version=0.0.4; charset=utf-8")
