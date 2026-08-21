<div align="center">

# 🩺⚡ AuraMed AI (Project DhanvantreAI)
### *Professional-Grade Clinical Decision Support & Medication Intelligence Platform*

[![Live Demo](https://img.shields.io/badge/Live_Demo-GitHub_Pages-brightgreen?style=for-the-badge&logo=github&logoColor=white)](https://rishisharma029.github.io/Project-DhanvantreAI/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139.2-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Security](https://img.shields.io/badge/Security-Hardened-red?style=for-the-badge&logo=shield&logoColor=white)](#-production-security--hardening)
[![Tests](https://img.shields.io/badge/Tests-667%2F667_Passed-34D399?style=for-the-badge&logo=pytest&logoColor=white)](#-automated-testing)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

</div>

---

## 🌐 Live Production Demo

Explore the live static frontend application featuring modern glassmorphism and dynamic UI enhancements:
👉 **[Launch Live Demo: https://rishisharma029.github.io/Project-DhanvantreAI/](https://rishisharma029.github.io/Project-DhanvantreAI/)**

- **Interactive AI Medical Chat**: [chat.html](https://rishisharma029.github.io/Project-DhanvantreAI/chat.html)
- **Clinical Dashboard**: [dashboard.html](https://rishisharma029.github.io/Project-DhanvantreAI/dashboard.html)
- **Medication Safety & Triage**: [medicines.html](https://rishisharma029.github.io/Project-DhanvantreAI/medicines.html)

---

## 📌 Executive Platform Overview

> **AuraMed AI** is a production-ready **Clinical Decision Support and Medication Information Platform**. It leverages advanced AI to retrieve evidence-based medical data, evaluate complex clinical conditions, perform multi-point medication safety audits, and assist healthcare professionals with transparent, grounded reasoning.

The platform integrates **Hybrid Dense/Lexical Retrieval (RAG)**, a **5-Stage Physician Decision Tree**, and a **Production-Grade Security Suite** to provide accurate clinical insights while maintaining the highest standards of data integrity and patient safety.

---

## 🏛️ System Architecture

```mermaid
graph TD
    User([👤 Patient / Clinician]) -->|HTTPS / WSS| Proxy[🛡️ NGINX Reverse Proxy]
    
    subgraph Core_Services [🐳 Docker Microservices]
        Proxy -->|/api/v1/*| API_Gateway[⚡ FastAPI Production Gateway]
        Proxy -->|/*| Web_UI[🌐 Liquid Glass Frontend]
        
        API_Gateway --> Auth[🔐 RBAC & Session Security]
        API_Gateway --> AI_Engine[🧠 Advanced AI Orchestrator]
        API_Gateway --> Payment[💳 Stripe Payment Infrastructure]
        API_Gateway --> Security[🛡️ Prompt Injection Guard]
        
        API_Gateway -->|Read/Write| DB[(🗄️ Medical Database)]
        API_Gateway -->|Cache| Cache[(🔴 Redis Cache)]
    end
```

---

## 🧠 Core AI & Clinical Engineering

### 1. 🔍 Advanced Multi-Modal AI Pipeline
*   **Document AI**: Automated extraction of lab entities from prescriptions and reports (CBC, Thyroid, etc.) with strict MIME and extension validation.
*   **Voice AI**: Real-time symptom analysis via voice interaction, integrated with core disease prediction engines.
*   **Image AI**: Multi-modal analysis for skin rashes and wound progression with built-in non-definitive clinical disclaimers.

### 2. 🩺 5-Stage Differential Reasoning Tree
The system follows a structured clinical path: **Evidence Collection** → **Differential Matrix** → **Rule-In/Rule-Out Logic** → **Severity Ranking** → **Triage Classification** (RED / URGENT / MODERATE / LOW).

### 3. 🛡️ 10-Point Medication Safety Audit
Audits dimensions including **Pregnancy (FDA Cat A-X)**, **Renal/Hepatic Function**, **Pediatrics/Geriatrics (Beers Criteria)**, and **FDA Black Box Warnings**.

---

## 🔐 Production Security & Hardening

AuraMed AI is built with a "Security First" philosophy, featuring multiple layers of protection:

| Security Layer | Implementation Detail |
| :--- | :--- |
| **Prompt Injection Guard** | 7-category detection system blocking jailbreaks, role-play hijacking, and system prompt leakage. |
| **Payment Integrity** | Stripe webhook HMAC-SHA256 verification and server-side price enforcement. |
| **Session Security** | Automatic session reset on password change and strict expiry for reset links. |
| **Infrastructure** | HSTS, CSRF Protection, Anti-Enumeration, and strict Upload Type Whitelisting. |

---

## 🎨 Professional UI/UX Enhancements
The frontend has been upgraded to a high-fidelity medical interface:
*   **Liquid Glass UI**: Modern glassmorphism effects across all feature cards.
*   **Dynamic Visuals**: Harsh gradients, animated rainbow borders, and glow effects.
*   **Professional Assets**: Full integration of **Lucide Icons** and enhanced typography.
*   **Responsive Themes**: Optimized Dark Mode and a pure white professional Light Mode.

---

## ⚙️ Technical Stack & Deployment

### 🐳 Quickstart with Docker
```bash
# Clone the repository
git clone https://github.com/Rishisharma029/Project-DhanvantreAI.git
cd Project-DhanvantreAI

# Launch the production stack
docker compose up -d --build
```

### 🧪 Automated Testing
The system maintains a comprehensive test suite ensuring 100% stability:
```bash
python -m pytest backend/tests --verbose
```
**Current Status**: `667 / 667 Passed (100% Pass Rate)`

---

## 📄 License & Clinical Disclaimer

This software is licensed under the MIT License.

**Clinical Disclaimer**: AuraMed AI is designed strictly as a Clinical Decision Support tool. It is not a substitute for professional medical judgment, diagnosis, or treatment. Always correlate AI findings with clinical evidence and physician consultation.
