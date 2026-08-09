"""
AuraMed AI — Entity Extraction Engine
=======================================
Extracts all structured clinical entities from free-text patient input.
Stores every entity only once — never asks for already-provided information again.
"""
import re
from typing import Dict, Any, List, Optional


def extract_entities(query_text: str, patient_age: Optional[int] = None,
                     patient_gender: Optional[str] = None) -> Dict[str, Any]:
    """
    Extracts structured clinical entities from raw query text.
    Returns a normalized entity dictionary used throughout the pipeline.
    """
    text = query_text.lower()
    entities: Dict[str, Any] = {}

    # ── Age ──────────────────────────────────────────────────────────────────
    if patient_age:
        entities["age"] = patient_age
    else:
        age_match = re.search(r"\b(?:age\s*:?\s*)?(\d{1,3})\s*(?:year|yr|yo|years?)?[\s\-]?old\b|\bage\s*:?\s*(\d{1,3})\b", text)
        if age_match:
            entities["age"] = int(age_match.group(1) or age_match.group(2))

    # ── Gender ───────────────────────────────────────────────────────────────
    if patient_gender:
        entities["gender"] = patient_gender.lower()
    else:
        if re.search(r"\b(?:sex|gender)\s*:?\s*f(?:emale)?\b", text) or any(w in text for w in ["female", "woman", "girl", "she", "her"]):
            entities["gender"] = "female"
        elif re.search(r"\b(?:sex|gender)\s*:?\s*m(?:ale)?\b", text) or any(w in text for w in ["male", "man", "boy", "he", "him"]):
            entities["gender"] = "male"

    # ── Temperature ──────────────────────────────────────────────────────────
    temp_match = re.search(r"(\d{2,3}(?:\.\d)?)\s*(?:°f|°c|f|c|degrees?)", text)
    if temp_match:
        entities["temperature"] = temp_match.group(1)
    elif any(w in text for w in ["high fever", "fever", "febrile", "pyrexia"]):
        entities["fever"] = True

    # ── Onset ─────────────────────────────────────────────────────────────────
    if any(w in text for w in ["suddenly", "sudden", "abrupt", "out of nowhere", "immediately"]):
        entities["onset"] = "sudden"
    elif any(w in text for w in ["gradually", "slowly", "over days", "over weeks"]):
        entities["onset"] = "gradual"

    # ── Duration ─────────────────────────────────────────────────────────────
    dur = re.search(r"(\d+)\s*(day|days|week|weeks|hour|hours|month|months)", text)
    if dur:
        entities["duration"] = f"{dur.group(1)} {dur.group(2)}"

    # ── Severity ──────────────────────────────────────────────────────────────
    if any(w in text for w in ["severe", "unbearable", "10/10", "worst", "extreme", "excruciating"]):
        entities["severity"] = "severe"
    elif any(w in text for w in ["moderate", "significant", "5/10", "6/10", "7/10"]):
        entities["severity"] = "moderate"
    elif any(w in text for w in ["mild", "slight", "minor", "1/10", "2/10", "3/10"]):
        entities["severity"] = "mild"

    # ── Key Red Flag Symptoms ─────────────────────────────────────────────────
    symptoms_detected = []
    SYMPTOM_KEYWORDS = [
        "fever", "cough", "headache", "sore throat", "runny nose", "fatigue",
        "body ache", "muscle ache", "shortness of breath", "chest pain", "chest tightness",
        "nausea", "vomiting", "diarrhea", "abdominal pain", "back pain", "joint pain",
        "neck stiffness", "stiff neck", "photophobia", "confusion", "seizure",
        "dizziness", "fainting", "palpitations", "sweating", "rash", "itching",
        "swelling", "weight loss", "loss of appetite", "frequent urination",
        "blood in urine", "blood in stool", "black stool", "loss of smell", "loss of taste",
        "wheezing", "stridor", "sneezing", "ear pain", "eye pain", "vision change",
    ]
    for sym in SYMPTOM_KEYWORDS:
        if sym in text:
            symptoms_detected.append(sym)
    if symptoms_detected:
        entities["detected_symptoms"] = symptoms_detected

    # ── Denied Symptoms (No X / Without X) ───────────────────────────────────
    denied = []
    deny_patterns = re.findall(r"no\s+(\w[\w\s]{1,30}?)(?:[,.]|$)", text)
    deny_patterns += re.findall(r"without\s+(\w[\w\s]{1,30}?)(?:[,.]|$)", text)
    deny_patterns += re.findall(r"denies?\s+(\w[\w\s]{1,30}?)(?:[,.]|$)", text)
    for d in deny_patterns:
        denied.append(d.strip())
    if denied:
        entities["denied_symptoms"] = denied

    # ── Pregnancy ─────────────────────────────────────────────────────────────
    if any(w in text for w in ["pregnant", "pregnancy", "weeks gestation", "trimester"]):
        entities["pregnancy"] = True
        wk = re.search(r"(\d+)\s*weeks?\s*(?:pregnant|gestation)", text)
        if wk:
            entities["gestational_weeks"] = int(wk.group(1))

    # ── Comorbidities ─────────────────────────────────────────────────────────
    comorbidities = []
    for cond in ["diabetes", "hypertension", "heart disease", "asthma", "copd",
                 "kidney disease", "liver disease", "hiv", "cancer", "epilepsy", "thyroid"]:
        if cond in text:
            comorbidities.append(cond)
    if comorbidities:
        entities["comorbidities"] = comorbidities

    # ── Travel History ────────────────────────────────────────────────────────
    if any(w in text for w in ["traveled", "travel", "returned from", "visited"]):
        entities["travel_history"] = True

    # ── Smoking ───────────────────────────────────────────────────────────────
    if any(w in text for w in ["smoker", "smoking", "cigarettes", "tobacco"]):
        entities["smoking"] = True

    return entities


def get_already_known_fields(entities: Dict[str, Any], req_age: Optional[int],
                              req_gender: Optional[str]) -> List[str]:
    """Returns list of entity fields already collected, so questions can be suppressed."""
    known = []
    if entities.get("age") or req_age:
        known.append("age")
    if entities.get("gender") or req_gender:
        known.append("gender")
    if entities.get("temperature") or entities.get("fever"):
        known.append("temperature")
    if entities.get("onset"):
        known.append("onset")
    if entities.get("duration"):
        known.append("duration")
    if entities.get("pregnancy"):
        known.append("pregnancy")
    return known
