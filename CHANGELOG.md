# CHANGELOG — AuraMed AI 🚀

All notable changes to the **AuraMed AI** platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.0.0] - 2026-08-02 — Major Clinical AI & Production Infrastructure Release 🎉

### Added
- **Module 4.1 — Advanced RAG Engine ⭐⭐⭐⭐⭐**: Hybrid BM25 + Vector Retrieval, Reciprocal Rank Fusion (RRF k=60), and Cross-Encoder re-ranking.
- **Module 4.2 — Medical Reasoning Engine ⭐⭐⭐⭐⭐**: 5-stage decision tree logic evaluating pathognomonic symptoms, Rule-In matches, and Rule-Out rejections.
- **Module 4.3 — Differential Diagnosis Engine ⭐⭐⭐⭐⭐**: Multi-candidate probability ranking (4+ diagnoses) with triage severity classification (`RED_EMERGENCY` to `LOW_MILD`).
- **Module 4.4 — Clinical Guideline Engine ⭐⭐⭐⭐⭐**: Evidence matching against WHO, CDC, NICE, ICMR, and FDA guidelines with section references.
- **Module 4.5 — Evidence Citation Engine ⭐⭐⭐⭐⭐**: 4-tier evidence mapping flagging unbacked statements as `[UNVERIFIED_STATEMENT]`.
- **Module 4.6 — Dual-Mode AI Explanation Engine ⭐⭐⭐⭐⭐**: Patient Mode (layperson clarity) vs Professional Mode (ICD-11, MOA, guidelines, contraindications).
- **Module 4.7 — Medication Safety AI ⭐⭐⭐⭐⭐**: 10-point audit for Pregnancy, Lactation, Pediatrics, Geriatrics (Beers Criteria), Renal/Hepatic adjustments, Allergies, QT Prolongation, Duplicate Therapy, and Black Box Warnings.
- **Module 4.8 — Clinical Timeline Engine ⭐⭐⭐⭐⭐**: Visual 5-stage trajectory (`SYMPTOMS` -> `ASSESSMENT` -> `MEDICINES` -> `FOLLOWUP` -> `RECOVERY`).
- **Module 4.9 — OCR & Document AI ⭐⭐⭐⭐⭐**: Document AI for CBC, Blood, Thyroid, Urine, MRI, and ECG lab reports.
- **Module 4.10 — Voice AI ⭐⭐⭐⭐⭐**: Speech-to-speech conversational triage pipeline.
- **Module 4.11 — Image AI (Future-Ready) ⭐⭐⭐⭐⭐**: Visual assessment for skin rashes, medication labels, and pill identification.
- **Module 4.12 — Follow-Up AI ⭐⭐⭐⭐⭐**: Patient follow-up continuity loop updating progression status (`IMPROVING`, `STABLE`, `WORSENING`, `RESOLVED`).
- **Module 4.14 — Personalized Health Insights ⭐⭐⭐⭐⭐**: Daily medication reminders, water tracking (2.5L-3.0L), and DASH lifestyle recommendations.
- **Module 4.15 — Explainability Dashboard ⭐⭐⭐⭐⭐**: 7-step step-by-step transparency trajectory.
- **Module 4.16 — AI Hallucination Guard ⭐⭐⭐⭐⭐**: Pre-response claim verification & auto-sanitization (`[REDACTED_UNVERIFIED_CLAIM]`).
- **Module 4.18 — Medical Knowledge Graph ⭐⭐⭐⭐⭐**: 6-tier entity graph (`Medicine` -> `Ingredient` -> `Disease` -> `Symptoms` -> `Interactions` -> `Side Effects`).
- **Module 4.19 — AI Quality Evaluation ⭐⭐⭐⭐⭐**: Automated measurement of Faithfulness, Groundedness, Citation Coverage, Consistency, and Safety.
- **Module 4.20 — AI Feedback & Continuous Improvement ⭐⭐⭐⭐⭐**: Feedback collection driving prompt optimization and RAG re-indexing.
- **Module 5.1 — Multi-Stage Docker Stack**: Production docker-compose with FastAPI, Nginx proxy, PostgreSQL 16, and Redis 7.
- **Module 5.2 — GitHub Actions CI/CD**: Automated Lint -> Security Scan -> Tests -> Docker Build -> Deploy pipeline.
- **Module 5.3 — Monitoring & Observability**: Prometheus metrics exporter (`/metrics`), `/health`, `/ready`, `/live` probes.
- **Module 5.4 — Structured Logging Engine**: HIPAA PHI sanitization and JSON formatted logging with correlation ID propagation.
- **Module 5.5 — Backup & Disaster Recovery**: AES-256 Fernet encrypted database backups with schema integrity verification.
- **Module 5.6 — Multi-Cloud Deployment Manifests**: Railway (`railway.json`), Render (`render.yaml`), AWS (`AppRunner.yaml`), GCP (`cloudrun-service.yaml`), and Azure (`azure-container-app.bicep`).
- **Module 5.7 — Interactive API Documentation**: OpenAPI 3.1, Swagger UI (`/docs`), and Redoc (`/redoc`).
- **Module 5.8 — Complete Documentation Suite**: `README.md`, `ARCHITECTURE.md`, `ER_DIAGRAM.md`, `API_GUIDE.md`, `DEPLOYMENT_GUIDE.md`, `SECURITY_GUIDE.md`, `AI_DESIGN.md`.
- **Module 5.9 — Performance Dashboard**: Live telemetry API (`/api/v1/performance/stats`) and real-time web dashboard (`/performance.html`).
- **Module 5.10 — AI Evaluation Dashboard**: Real-time visualization of Hallucination Rate, Citation Coverage, Groundedness, Faithfulness, and Safety Scores (`/ai_eval.html`).
- **Module 5.11 — Production Security**: Penetration testing suite for SQL Injection, XSS, HTTPS enforcement, and secret key rotation.

---

## [v1.1.0] - 2026-07-15 — System Hardening & Gateway Performance

### Added
- PostgreSQL 16 migration support and Redis caching layer.
- Gateway rate limiter (100 req/min) and system audit log service.
- Role-Based Access Control (RBAC) supporting Patient, Doctor, Pharmacist, and Admin roles.

---

## [v1.0.0] - 2026-06-01 — Initial Base Release

### Added
- Initial FastAPI application boilerplate.
- Basic database tables for Users, Medicines, Diseases, and Symptoms.
- Authentication endpoints (`/auth/register`, `/auth/login`).
