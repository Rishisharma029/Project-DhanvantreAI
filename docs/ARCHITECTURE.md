# AuraMed AI — System Architecture & Component Design 🏛️

## 1. High-Level Architecture Overview

AuraMed AI is structured as a decoupled microservices-ready monolith using FastAPI, PostgreSQL, Redis, Nginx, and multi-modal AI reasoning engines.

```
                               ┌─────────────────────────┐
                               │     Web Clients         │
                               │  (Patients / Doctors)   │
                               └────────────┬────────────┘
                                            │ HTTP / HTTPS / WS
                                            ▼
                               ┌─────────────────────────┐
                               │  Nginx Reverse Proxy    │
                               │  (Port 80 / 443)        │
                               └────────────┬────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               │                            │                            │
               ▼                            ▼                            ▼
┌─────────────────────────────┐ ┌─────────────────────────┐ ┌──────────────────────────┐
│  API Gateway & Auth         │ │  Clinical AI Engines    │ │  Monitoring & Telemetry  │
│  • JWT Auth & RBAC          │ │  • Advanced RAG Engine  │ │  • Prometheus Exporter   │
│  • Rate Limiting (100r/m)   │ │  • Differential Diagnosis│ │  • Performance Dashboard │
│  • Audit Logging Middleware │ │  • Medication Safety AI │ │  • Structured JSON Logs  │
└──────────────┬──────────────┘ └────────────┬────────────┘ └────────────┬─────────────┘
               │                             │                           │
               ▼                             ▼                           ▼
┌─────────────────────────────┐ ┌─────────────────────────┐ ┌──────────────────────────┐
│  PostgreSQL Database        │ │  Redis Cache Layer      │ │  Knowledge Base          │
│  • Users, Profiles, History │ │  • RAG Query Cache      │ │  • Medical Knowledge Graph│
│  • Clinical Audit Logs      │ │  • Token Blacklist      │ │  • Evidence Citations    │
└─────────────────────────────┘ └─────────────────────────┘ └──────────────────────────┘
```

## 2. Core Subsystems

### 2.1 API Gateway & Security Layer
- Enforces OAuth2 Password Grant with JWT Access and Refresh Tokens.
- Role-Based Access Control (RBAC: `patient`, `doctor`, `pharmacist`, `admin`).
- Rate Limiting (100 requests per minute per IP).

### 2.2 Clinical Reasoning Core
- **Advanced RAG Engine**: Hybrid BM25 + Dense Vector Search + Reciprocal Rank Fusion (RRF).
- **Differential Reasoning**: Rule-In / Rule-Out physician decision trees with pathognomonic symptom analysis.
- **Medication Safety AI**: 10-point audit verifying drug-drug, drug-disease, pregnancy, lactation, renal, hepatic, and beers criteria contraindications.

### 2.3 Storage & Persistence
- **PostgreSQL**: Primary transactional store for user accounts, medical profiles, consultation sessions, and audit events.
- **Redis**: Caching vector query embeddings, rate limit counters, and JWT revocation blacklists.
