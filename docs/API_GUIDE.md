# AuraMed AI — API Integration Guide 🔌

## 1. Interactive API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI 3.1 Spec**: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## 2. Authentication Protocol

All secure endpoints require a `Bearer <token>` HTTP header.

### 2.1 Register New Account
`POST /api/v1/auth/register`
```json
{
  "email": "doctor@hospital.org",
  "password": "SecurePassword123!",
  "full_name": "Dr. Sarah Jenkins",
  "role": "doctor"
}
```

### 2.2 Login & Receive Token
`POST /api/v1/auth/login`
```json
{
  "email": "doctor@hospital.org",
  "password": "SecurePassword123!"
}
```
**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "refresh_token": "a4f8c...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 3. Key Clinical API Endpoints

### 3.1 Medical Reasoning Evaluation
`POST /api/v1/reasoning/evaluate`
Evaluates symptoms using 5-stage decision tree logic.

### 3.2 Multi-Candidate Differential Diagnosis
`POST /api/v1/differential/diagnose`
Calculates probability rankings across 4+ candidate diseases.

### 3.3 10-Point Medication Safety Audit
`POST /api/v1/med-safety/evaluate`
Performs comprehensive safety audit for pregnancy, geriatrics, renal, hepatic, and black box warnings.
