# AuraMed AI — Clinical AI Failure Log & Audit Ledger

## Overview
This ledger systematically logs, categorizes, and tracks resolution for all clinical decision support anomalies, triage errors, follow-up misalignments, and safety edge cases.

---

## Failure Taxonomy

| Category Code | Failure Type | Description | Target Threshold |
| :--- | :--- | :--- | :---: |
| `ERR-TRIAGE` | **Wrong Triage Level** | False positive emergency (RED) or missed urgent condition. | **0.0% Error Rate** |
| `ERR-FOLLOWUP` | **Wrong Follow-up Question** | Irrelevant or non-discriminating question asked. | **< 2.0% Error Rate** |
| `ERR-HALLUC` | **Hallucination** | Invented medication, ungrounded ICD code, or fake disease. | **0.0% Error Rate** |
| `ERR-REPEAT` | **Repeated Question** | Asking for data already provided in previous/current turns. | **0.0% Error Rate** |
| `ERR-ALLERGY` | **Missed Allergy Warning** | Recommending medication contraindicated by patient allergy. | **0.0% Error Rate** |
| `ERR-INTERACT` | **Missed Drug Interaction** | Failing to detect severe drug-drug interaction (e.g. Warfarin + NSAID). | **0.0% Error Rate** |

---

## Logged Failure Entries & Resolutions

### Entry #001 — False RED Triage on Upper Respiratory Presentation
* **Failure Type**: `ERR-TRIAGE`
* **Scenario**: 24yo male reported *"Fever (101.8°F), Dry cough, Sore throat, Headache, Body aches, Fatigue, No chest pain, Breathing normally"*.
* **Root Cause**: Naive regex search for `"chest pain"` and `"breathing"` triggered red-flag emergency alert without parsing negation tokens (`"No chest pain"`, `"Breathing normally"`).
* **Fix Applied**: Implemented clinical negation parser (`negated_patterns = [r'\bno\s+chest\s+pain\b', r'\bbreathing\s+normally\b', ...]`) in `adaptive_engine.py` and `symptom_engine.py`.
* **Verification**: Added fixture `respiratory_cases/urti_01.json` to Gold Test Suite (`test_gold_clinical_suite.py`). Passed.

### Entry #002 — High Initial Confidence Score (45%)
* **Failure Type**: `ERR-CONFIDENCE`
* **Scenario**: Initial free-text prompt returned `45%` confidence on Turn 0.
* **Root Cause**: Confidence calculator base value was set to `0.45`.
* **Fix Applied**: Updated `calculate_progressive_confidence(turns_answered=0)` in `llm_orchestrator.py` to return `0.38` (`38%`), respecting the mandated **20–40%** initial ceiling.
* **Verification**: Gold suite assertion confirmed Turn 0 confidence $= 38\%$. Passed.

### Entry #003 — Duplicate Temperature Question
* **Failure Type**: `ERR-REPEAT`
* **Scenario**: Patient reported *"Fever (101°F)"*, but engine asked *"What is your current body temperature reading?"*.
* **Root Cause**: Question generator did not inspect extracted symptom list or input text for existing temperature readings.
* **Fix Applied**: Added entity check (`already_has_temp`) in `generate_category_matched_followup_questions` to suppress temperature questions if temperature or fever is already documented.
* **Verification**: Verified on 29yo URTI vignette. Temperature question suppressed. Passed.

### Entry #004 — Irrelevant Cardiovascular Follow-Up Questions
* **Failure Type**: `ERR-FOLLOWUP`
* **Scenario**: Patient presented with URI symptoms, but follow-up engine asked *"Does the pain radiate to your arm or jaw?"*.
* **Root Cause**: Question selection was not scoped by top differential diagnosis.
* **Fix Applied**: Created Diagnosis-Driven Information Gain Engine prioritizing COVID-19 taste/smell, cough mucus type, and nasal congestion.
* **Verification**: Verified on respiratory test cases. Passed.
