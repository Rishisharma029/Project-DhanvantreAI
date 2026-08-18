import time
import sqlite3
from typing import Optional
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.database import init_user_db, settings as db_settings
from app.api.auth_router import router as auth_router
from app.api.profile_router import router as profile_router
from app.api.session_router import router as session_router
from app.api.symptom_router import router as symptom_router
from app.api.adaptive_router import router as adaptive_router
from app.api.disease_router import router as disease_router
from app.api.medicine_router import router as medicine_router
from app.api.recommendation_router import router as recommendation_router
from app.api.interaction_router import router as interaction_router
from app.api.safety_router import router as safety_router
from app.api.dosage_router import router as dosage_router
from app.api.search_router import router as search_router
from app.api.knowledge_router import router as knowledge_router
from app.api.orchestrator_router import router as orchestrator_router
from app.api.guardrail_router import router as guardrail_router
from app.api.explainability_router import router as explainability_router
from app.api.confidence_router import router as confidence_router
from app.api.history_router import router as history_router
from app.api.notification_router import router as notification_router
from app.api.universal_search_router import router as universal_search_router
from app.api.admin_router import router as admin_router
from app.api.analytics_router import router as analytics_router
from app.api.audit_router import router as audit_router
from app.api.task_router import router as task_router
from app.api.cache_router import router as cache_router
from app.api.gateway_router import router as gateway_router
from app.api.rag_router import router as rag_router
from app.api.reasoning_router import router as reasoning_router
from app.api.differential_router import router as differential_router
from app.api.guideline_router import router as guideline_router
from app.api.evidence_router import router as evidence_router
from app.api.explanation_router import router as explanation_router
from app.api.med_safety_router import router as med_safety_router
from app.api.timeline_router import router as timeline_router
from app.api.hallucination_guard_router import router as hallucination_guard_router
from app.api.knowledge_graph_router import router as knowledge_graph_router
from app.api.feedback_router import router as feedback_router
from app.api.quality_evaluation_router import router as quality_evaluation_router
from app.api.insights_router import router as insights_router
from app.api.explainability_dashboard_router import router as explainability_dashboard_router
from app.api.followup_router import router as followup_router
from app.api.document_router import router as document_router
from app.api.voice_router import router as voice_router
from app.api.image_router import router as image_router
from app.api.monitoring_router import router as monitoring_router
from app.api.disaster_recovery_router import router as disaster_recovery_router
from app.api.performance_router import router as performance_router
from app.api.ai_eval_dashboard_router import router as ai_eval_dashboard_router
from app.api.clinical_eval_router import router as clinical_eval_router
from app.api.v1.eval_dashboard import router as eval_dashboard_router
from app.middleware.monitoring_middleware import MonitoringMiddleware
from app.services.api_gateway_service import gateway_rate_limiter














from app.services.audit_service import log_system_audit_event

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema on startup
    init_user_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 1. Response Compression Middleware (GZip >= 500 bytes)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(MonitoringMiddleware)

# 2. Configure CORS (Domain-Restricted Production Policy)
allowed_origins = settings.CORS_ORIGINS if (settings.ENVIRONMENT == "production" or os.getenv("CORS_ORIGINS")) else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With", "Accept", "Origin"],
)


# 3. HTTPS Enforcement & Security Headers Middleware
@app.middleware("http")
async def security_https_middleware(request: Request, call_next):
    # Check for HTTP scheme or X-Forwarded-Proto header
    proto = request.headers.get("x-forwarded-proto", request.url.scheme).lower()
    is_http = proto == "http"

    # Enforce HTTPS in production or when ENFORCE_HTTPS configuration is enabled
    if (settings.ENFORCE_HTTPS or settings.ENVIRONMENT == "production") and is_http:
        # Block authentication endpoints over plain HTTP strictly
        if request.url.path.startswith(f"{settings.API_V1_STR}/auth"):
            return Response(
                content='{"detail": "Authentication over plain HTTP is forbidden. Secure HTTPS connection required."}',
                status_code=403,
                media_type="application/json"
            )
        # Redirect all other HTTP traffic to HTTPS with 301 Permanent Redirect
        https_url = request.url.replace(scheme="https")
        return Response(
            status_code=301,
            headers={"Location": str(https_url)}
        )

    response = await call_next(request)

    # Attach Full Production Security Headers Suite & HSTS
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'none'; "
        "object-src 'none';"
    )
    
    response.headers["Content-Security-Policy"] = csp_policy
    response.headers["Permissions-Policy"] = "geolocation=(self), microphone=(), camera=(), payment=(), display-capture=()"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


# 4. Gateway Rate Limiting & Audit Middleware
@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Bypass rate limit for OpenAPI docs, health check, and testclient test suite runner
    if not request.url.path.startswith("/docs") and not request.url.path.startswith("/openapi") and client_ip != "testclient":
        is_allowed, remaining, reset_sec = gateway_rate_limiter.check_rate_limit(client_ip)
        if not is_allowed:
            return Response(
                content='{"detail": "Rate limit exceeded. Maximum 100 requests per minute allowed."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "X-RateLimit-Limit": "100",
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(reset_sec)
                }
            )

    response = await call_next(request)
    duration_ms = int((time.time() - start_time) * 1000)


    # Attach Gateway Rate Limit Headers
    response.headers["X-RateLimit-Limit"] = "100"

    # Silent Audit Log
    if not request.url.path.startswith("/docs") and not request.url.path.startswith("/openapi"):
        try:
            conn = sqlite3.connect(db_settings.DATABASE_PATH, timeout=5.0)
            log_type = "ERROR" if response.status_code >= 400 else "API_REQUEST"
            log_system_audit_event(
                user_id=0,
                log_type=log_type,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                latency_ms=duration_ms,
                message=f"HTTP {request.method} {request.url.path} -> {response.status_code}",
                details_json="{}",
                db=conn
            )
            conn.close()
        except Exception:
            pass

    return response

def _get_frontend_file(filename: str) -> Optional[str]:
    candidates = [
        os.path.join(os.getcwd(), "frontend", filename),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", filename)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", filename)),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

@app.get("/")
@app.get("/index.html")
def root():
    frontend_index = _get_frontend_file("index.html")
    if frontend_index:
        return FileResponse(frontend_index)
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/landing")
def landing_page():
    frontend_index = _get_frontend_file("index.html")
    if frontend_index:
        return FileResponse(frontend_index)
    return {"error": "Landing page not found"}

@app.get("/auth")
@app.get("/auth.html")
def auth_page():
    auth_index = _get_frontend_file("auth.html")
    if auth_index:
        return FileResponse(auth_index)
    return {"error": "Auth page not found"}

@app.get("/dashboard")
@app.get("/dashboard.html")
def dashboard_page():
    dash_index = _get_frontend_file("dashboard.html")
    if dash_index:
        return FileResponse(dash_index)
    return {"error": "Dashboard page not found"}

@app.get("/chat")
@app.get("/chat.html")
def chat_page():
    chat_index = _get_frontend_file("chat.html")
    if chat_index:
        return FileResponse(chat_index)
    return {"error": "Chat page not found"}

@app.get("/wizard")
@app.get("/wizard.html")
def wizard_page():
    wiz_index = _get_frontend_file("wizard.html")
    if wiz_index:
        return FileResponse(wiz_index)
    return {"error": "Wizard page not found"}

@app.get("/medicines")
@app.get("/medicines.html")
def medicines_page():
    med_index = _get_frontend_file("medicines.html")
    if med_index:
        return FileResponse(med_index)
    return {"error": "Medicines page not found"}

@app.get("/diseases")
@app.get("/diseases.html")
def diseases_page():
    dis_index = _get_frontend_file("diseases.html")
    if dis_index:
        return FileResponse(dis_index)
    return {"error": "Diseases page not found"}

@app.get("/interactions")
@app.get("/interactions.html")
def interactions_page():
    inter_index = _get_frontend_file("interactions.html")
    if inter_index:
        return FileResponse(inter_index)
    return {"error": "Interactions page not found"}

@app.get("/results")
@app.get("/results.html")
def results_page():
    res_index = _get_frontend_file("results.html")
    if res_index:
        return FileResponse(res_index)
    return {"error": "Results page not found"}

@app.get("/explainability")
@app.get("/explainability.html")
def explainability_page():
    exp_index = _get_frontend_file("explainability.html")
    if exp_index:
        return FileResponse(exp_index)
    return {"error": "Explainability page not found"}

@app.get("/report_viewer")
@app.get("/report_viewer.html")
def report_viewer_page():
    rep_index = _get_frontend_file("report_viewer.html")
    if rep_index:
        return FileResponse(rep_index)
    return {"error": "Report viewer page not found"}

@app.get("/history")
@app.get("/history.html")
def history_page():
    hist_index = _get_frontend_file("history.html")
    if hist_index:
        return FileResponse(hist_index)
    return {"error": "History page not found"}

@app.get("/profile")
@app.get("/profile.html")
def profile_page():
    prof_index = _get_frontend_file("profile.html")
    if prof_index:
        return FileResponse(prof_index)
    return {"error": "Profile page not found"}

@app.get("/settings")
@app.get("/settings.html")
def settings_page():
    sett_index = os.path.join(os.getcwd(), "frontend", "settings.html")
    if os.path.exists(sett_index):
        return FileResponse(sett_index)
    return {"error": "Settings page not found"}

@app.get("/emergency")
@app.get("/emergency.html")
def emergency_page():
    em_index = os.path.join(os.getcwd(), "frontend", "emergency.html")
    if os.path.exists(em_index):
        return FileResponse(em_index)
    return {"error": "Emergency page not found"}

@app.get("/responsive")
@app.get("/responsive.html")
def responsive_page():
    resp_index = _get_frontend_file("responsive.html")
    if resp_index:
        return FileResponse(resp_index)
    return {"error": "Responsive page not found"}

@app.get("/accessibility")
@app.get("/accessibility.html")
def accessibility_page():
    access_index = _get_frontend_file("accessibility.html")
    if access_index:
        return FileResponse(access_index)
    return {"error": "Accessibility page not found"}

@app.get("/states")
@app.get("/states.html")
def states_page():
    st_index = _get_frontend_file("states.html")
    if st_index:
        return FileResponse(st_index)
    return {"error": "States page not found"}

@app.get("/notifications")
@app.get("/notifications.html")
def notifications_page():
    notif_index = _get_frontend_file("notifications.html")
    if notif_index:
        return FileResponse(notif_index)
    return {"error": "Notifications page not found"}

# Unauthenticated admin page routes removed for security hardening

@app.get("/performance")
@app.get("/performance.html")
def performance_page():
    perf_index = _get_frontend_file("performance.html")
    if perf_index:
        return FileResponse(perf_index)
    return {"error": "Performance dashboard not found"}

@app.get("/ai_eval")
@app.get("/ai_eval.html")
def ai_eval_page():
    eval_index = _get_frontend_file("ai_eval.html")
    if eval_index:
        return FileResponse(eval_index)
    return {"error": "AI evaluation dashboard not found"}

@app.get("/{asset_name:path}.css")
def serve_css(asset_name: str):
    file_path = _get_frontend_file(f"{asset_name}.css")
    if file_path:
        return FileResponse(file_path, media_type="text/css")
    return {"error": "CSS file not found"}

@app.get("/{asset_name:path}.js")
def serve_js(asset_name: str):
    file_path = _get_frontend_file(f"{asset_name}.js")
    if file_path:
        return FileResponse(file_path, media_type="application/javascript")
    return {"error": "JS file not found"}

frontend_dir = None
for p in [
    os.path.join(os.getcwd(), "frontend"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend")),
]:
    if os.path.exists(p):
        frontend_dir = p
        break

class NoDirectoryListingStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            full_path = self.get_path(path)
            if os.path.isdir(full_path):
                return Response(content='{"detail": "Directory listing is forbidden."}', status_code=403, media_type="application/json")
        except Exception:
            pass
        return await super().get_response(path, scope)

if frontend_dir:
    app.mount("/static", NoDirectoryListingStaticFiles(directory=frontend_dir), name="static")

# Include Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(profile_router, prefix=settings.API_V1_STR)
app.include_router(session_router, prefix=settings.API_V1_STR)
app.include_router(symptom_router, prefix=settings.API_V1_STR)
app.include_router(adaptive_router, prefix=settings.API_V1_STR)
app.include_router(disease_router, prefix=settings.API_V1_STR)
app.include_router(medicine_router, prefix=settings.API_V1_STR)
app.include_router(recommendation_router, prefix=settings.API_V1_STR)
app.include_router(interaction_router, prefix=settings.API_V1_STR)
app.include_router(safety_router, prefix=settings.API_V1_STR)
app.include_router(dosage_router, prefix=settings.API_V1_STR)
app.include_router(search_router, prefix=settings.API_V1_STR)
app.include_router(knowledge_router, prefix=settings.API_V1_STR)
app.include_router(orchestrator_router, prefix=settings.API_V1_STR)
app.include_router(guardrail_router, prefix=settings.API_V1_STR)
app.include_router(explainability_router, prefix=settings.API_V1_STR)
app.include_router(confidence_router, prefix=settings.API_V1_STR)
app.include_router(history_router, prefix=settings.API_V1_STR)
app.include_router(notification_router, prefix=settings.API_V1_STR)
app.include_router(universal_search_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)
app.include_router(task_router, prefix=settings.API_V1_STR)
app.include_router(cache_router, prefix=settings.API_V1_STR)
app.include_router(gateway_router, prefix=settings.API_V1_STR)
app.include_router(rag_router, prefix=settings.API_V1_STR)
app.include_router(reasoning_router, prefix=settings.API_V1_STR)
app.include_router(differential_router, prefix=settings.API_V1_STR)
app.include_router(guideline_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(explanation_router, prefix=settings.API_V1_STR)
app.include_router(med_safety_router, prefix=settings.API_V1_STR)
app.include_router(timeline_router, prefix=settings.API_V1_STR)
app.include_router(hallucination_guard_router, prefix=settings.API_V1_STR)
app.include_router(knowledge_graph_router, prefix=settings.API_V1_STR)
app.include_router(feedback_router, prefix=settings.API_V1_STR)
app.include_router(quality_evaluation_router, prefix=settings.API_V1_STR)
app.include_router(insights_router, prefix=settings.API_V1_STR)
app.include_router(explainability_dashboard_router, prefix=settings.API_V1_STR)
app.include_router(followup_router, prefix=settings.API_V1_STR)
app.include_router(document_router, prefix=settings.API_V1_STR)
app.include_router(voice_router, prefix=settings.API_V1_STR)
app.include_router(image_router, prefix=settings.API_V1_STR)
app.include_router(disaster_recovery_router, prefix=settings.API_V1_STR)
app.include_router(performance_router, prefix=settings.API_V1_STR)
app.include_router(ai_eval_dashboard_router, prefix=settings.API_V1_STR)
app.include_router(clinical_eval_router, prefix=settings.API_V1_STR)
app.include_router(eval_dashboard_router, prefix=settings.API_V1_STR)
app.include_router(monitoring_router)














from app.api.payment_router import router as payment_router
app.include_router(payment_router, prefix=settings.API_V1_STR)
