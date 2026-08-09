# AuraMed AI — Security & HIPAA PHI Protection Guide 🛡️

## 1. Compliance Directives & PHI Protection

- **Rule 1 (No PHI Logging)**: System logs must NEVER record protected health information (patient names, raw symptom arrays, SSNs, credit cards). The `StructuredLogger` automatically redacts sensitive patterns into `[REDACTED_PHI]`.
- **Rule 2 (No Authentication over HTTP)**: Plain HTTP authentication requests (`/auth/login`, `/auth/register`) are forbidden and rejected with `403 Forbidden`. HTTPS is mandatory.
- **Rule 3 (Database Backup Encryption)**: Database snapshots are encrypted using **AES-256 Fernet symmetric key encryption** with SHA-256 integrity verification.

## 2. API Gateway & Transport Security

- **Strict Transport Security (HSTS)**: `max-age=31536000; includeSubDomains; preload`
- **Content Security Policy (CSP)**: Domain-restricted script, style, font, and frame-ancestors policies.
- **Rate Limiting**: 100 requests per minute per IP enforced via `gateway_rate_limiter` and Nginx `limit_req_zone`.
- **Audit Logging**: Every API request and security event is recorded in `system_audit_logs`.
