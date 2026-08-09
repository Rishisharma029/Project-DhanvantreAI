import re
import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.symptom_schema import ExtractedSymptomItem, CandidateDiseaseMatch

SYMPTOM_SYNONYMS = {
    'head pain': 'headache',
    'head ache': 'headache',
    'headaches': 'headache',
    'high temp': 'fever',
    'high temperature': 'fever',
    'feverish': 'fever',
    'high fever': 'fever',
    'severe fever': 'fever',
    'pyrexia': 'fever',
    'fevers': 'fever',
    'puking': 'vomiting',
    'throwing up': 'vomiting',
    'nauseous': 'nausea',
    'feeling sick': 'nausea',
    'stomach ache': 'stomach pain',
    'belly ache': 'stomach pain',
    'abdominal pain': 'stomach pain',
    'tummy pain': 'stomach pain',
    'stomach pain': 'stomach pain',
    'joint pain': 'joint pain',
    'body ache': 'body ache',
    'body pain': 'joint pain',
    'muscle pain': 'muscle pain',
    'skin eruption': 'skin rash',
    'rashes': 'skin rash',
    'rash': 'skin rash',
    'cold': 'continuous sneezing',
    'sneezing': 'continuous sneezing',
    'cough': 'cough',
    'chills': 'chills',
    'shivering': 'shivering',
    'fatigue': 'fatigue',
    'tiredness': 'fatigue',
    'weakness': 'fatigue',
    'chest pain': 'chest pain',
    'shortness of breath': 'breathlessness',
    'difficulty breathing': 'breathlessness',
    'breathless': 'breathlessness',
    'loose motion': 'diarrhoea',
    'diarrhea': 'diarrhoea',
    'diarrhoea': 'diarrhoea',
    'itching': 'itching',
    'itchy': 'itching',
    'throat pain': 'sore throat',
    'sore throat': 'sore throat'
}

SEVERITY_MODIFIERS = {
    'high': 'Severe',
    'severe': 'Severe',
    'intense': 'Severe',
    'extreme': 'Severe',
    'unbearable': 'Emergency',
    'very high': 'Severe',
    'acute': 'Severe',
    'mild': 'Mild',
    'slight': 'Mild',
    'light': 'Mild',
    'moderate': 'Moderate'
}

def detect_severity_modifier(phrase: str) -> str:
    """Detect severity modifier from query phrase."""
    phrase_lower = phrase.lower()
    for mod, sev in SEVERITY_MODIFIERS.items():
        if re.search(rf'\b{mod}\b', phrase_lower):
            return sev
    return "Moderate"

def clean_canonical_name(name: str) -> str:
    """Remove intensity prefixes like 'high', 'severe', 'mild' from symptom names."""
    clean = re.sub(r'^(high|severe|mild|intense|acute|slight|very high)\s+', '', name.strip(), flags=re.IGNORECASE)
    return clean.strip().title()

def extract_and_normalize_symptoms(text: str, db: sqlite3.Connection) -> List[ExtractedSymptomItem]:
    """
    Extract, normalize, map synonyms, detect severity, and deduplicate symptoms from free-form text.
    """
    if not text or not isinstance(text, str):
        return []

    text_lower = text.lower()
    
    # Strip explicit negations so "no chest pain", "breathing normally" are not extracted as active symptoms
    negated_patterns = [
        r'\bno\s+chest\s+pain\b', r'\bwithout\s+chest\s+pain\b', r'\bdenies\s+chest\s+pain\b',
        r'\bbreathing\s+normally\b', r'\bnormal\s+breathing\b', r'\bno\s+breathing\s+difficulty\b',
        r'\bno\s+shortness\s+of\s+breath\b', r'\bno\s+allergies\b', r'\bno\s+medicines\b', r'\bno\s+medications\b'
    ]
    for p in negated_patterns:
        text_lower = re.sub(p, '', text_lower)

    extracted_map = {}

    cursor = db.cursor()
    cursor.execute("SELECT name, severity_weight FROM symptoms;")
    db_symptoms = {row[0].lower(): (row[0], row[1]) for row in cursor.fetchall()}

    # 1. Check synonym dictionary
    for term, canonical in SYMPTOM_SYNONYMS.items():
        if re.search(rf'\b{re.escape(term)}\b', text_lower):
            db_entry = db_symptoms.get(canonical.lower())
            canon_name = db_entry[0] if db_entry else canonical.title()
            weight = db_entry[1] if db_entry else 1
            
            sev = detect_severity_modifier(text_lower)
            extracted_map[canon_name.lower()] = ExtractedSymptomItem(
                raw_term=term,
                canonical_name=clean_canonical_name(canon_name),
                severity=sev,
                severity_weight=weight
            )

    # 2. Direct DB Canonical Symptom matching
    for sym_lower, (sym_orig, weight) in db_symptoms.items():
        if len(sym_lower) < 3: continue
        pattern = rf'\b{re.escape(sym_lower)}\b'
        if re.search(pattern, text_lower):
            canon_clean = clean_canonical_name(sym_orig)
            if canon_clean.lower() not in extracted_map:
                sev = detect_severity_modifier(text_lower)
                extracted_map[canon_clean.lower()] = ExtractedSymptomItem(
                    raw_term=sym_orig,
                    canonical_name=canon_clean,
                    severity=sev,
                    severity_weight=weight
                )

    return list(extracted_map.values())

def find_candidate_diseases(symptom_names: List[str], db: sqlite3.Connection) -> List[CandidateDiseaseMatch]:
    """
    Match extracted canonical symptoms against Phase 1 disease_symptoms junction database table.
    Calculates disease match percentage.
    """
    if not symptom_names:
        return []

    cursor = db.cursor()
    
    # Query with exact or substring symptom match
    query_syms = [s.lower() for s in symptom_names]
    placeholders = ",".join(["?"] * len(query_syms))
    
    cursor.execute(f"SELECT id, name FROM symptoms WHERE LOWER(name) IN ({placeholders});", query_syms)
    sym_rows = cursor.fetchall()
    
    # Also search LIKE for cleaned names e.g. 'fever'
    if not sym_rows:
        like_clauses = " OR ".join(["LOWER(name) LIKE ?"] * len(query_syms))
        cursor.execute(f"SELECT id, name FROM symptoms WHERE {like_clauses};", [f"%{s}%" for s in query_syms])
        sym_rows = cursor.fetchall()

    if not sym_rows:
        return []

    sym_ids = list(set(row[0] for row in sym_rows))
    sym_id_placeholders = ",".join(["?"] * len(sym_ids))

    query = f"""
        SELECT d.name, d.severity_level, d.description,
               COUNT(ds.symptom_id) as matched_count,
               (SELECT COUNT(*) FROM disease_symptoms WHERE disease_id = d.id) as total_count
        FROM diseases d
        JOIN disease_symptoms ds ON d.id = ds.disease_id
        WHERE ds.symptom_id IN ({sym_id_placeholders})
        GROUP BY d.id
        ORDER BY matched_count DESC, total_count ASC
        LIMIT 5;
    """
    cursor.execute(query, sym_ids)
    
    candidates = []
    for row in cursor.fetchall():
        d_name, d_sev, d_desc, matched_c, total_c = row
        pct = round((matched_c / total_c) * 100.0, 1) if total_c > 0 else 0.0
        candidates.append(CandidateDiseaseMatch(
            disease_name=d_name,
            matched_symptoms_count=matched_c,
            total_disease_symptoms=total_c,
            match_percentage=pct,
            severity_level=d_sev or "Moderate",
            description=d_desc or ""
        ))

    return candidates
