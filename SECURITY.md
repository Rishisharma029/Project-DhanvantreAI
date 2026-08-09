# Security Policy — AuraMed AI 🛡️

## 1. Positioning & Intent

**AuraMed AI** is an AI-powered **Clinical Decision Support and Medication Information Platform** that retrieves evidence-based information, evaluates possible conditions, performs medication safety checks, and assists users and healthcare professionals through transparent reasoning and structured reports.

Given the healthcare domain of this platform, security, data privacy, and HIPAA compliance are primary design imperatives.

---

## 2. Core Security Controls

- **No Protected Health Information (PHI) Logging**: Logs are strictly sanitized using regex-based PHI scrubbing (`sanitize_phi()`). Patient names, raw symptom arrays, SSNs, credit cards, emails, and credentials are automatically redacted into `[REDACTED_PHI]`.
- **HTTPS Enforcement**: Plain HTTP authentication requests (`/api/v1/auth/login`, `/api/v1/auth/register`) are blocked with `403 Forbidden`. HTTPS with TLS 1.3 is mandatory.
- **Transport Security Headers**:
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
  - `Content-Security-Policy: default-src 'self'; script-src 'self' ...`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
- **Database Backup Encryption**: Database snapshots are encrypted using **AES-256 Fernet symmetric key encryption** with SHA-256 integrity verification.
- **API Gateway Rate Limiting**: Enforces a strict rate limit of 100 requests per minute per IP address.
- **Role-Based Access Control (RBAC)**: Enforces role checks (`patient`, `doctor`, `pharmacist`, `admin`).

---

## 3. Reporting a Vulnerability

We take the security of AuraMed AI seriously. If you believe you have discovered a security vulnerability, please do NOT open a public GitHub issue.

Please report vulnerabilities privately via email to:
📧 **security@auramed.ai** or **rishi.sharma029@gmail.com**

### What to Include in Your Report:
- Type of vulnerability (e.g., SQLi, XSS, SSRF, Auth Bypass)
- Step-by-step proof-of-concept (PoC) or script
- Potential impact of the vulnerability

We will acknowledge receipt within 24 hours and provide a timeline for resolution.
