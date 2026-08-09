import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.disease_schema import PredictedDiseaseItem, DiseasePredictResponse

def clean_symptom_token(sym: str) -> str:
    """Normalize symptom token string."""
    return sym.strip().replace('_', ' ').lower()

def predict_diseases_from_symptoms(symptoms: List[str], top_n: int, db: sqlite3.Connection) -> DiseasePredictResponse:
    """
    Core Disease Prediction Engine logic:
    - Resolves symptom IDs and names
    - Calculates Jaccard & Weighted Match Ratios
    - Separates matching symptoms vs missing symptoms for differential diagnosis
    - Returns top diseases ordered by confidence
    """
    if not symptoms:
        return DiseasePredictResponse(input_symptoms=[], total_matches_found=0, top_diseases=[])

    clean_inputs = [clean_symptom_token(s) for s in symptoms if s.strip()]
    cursor = db.cursor()

    # 1. Resolve Input Symptoms in DB
    placeholders = ",".join(["?"] * len(clean_inputs))
    cursor.execute(f"SELECT id, name FROM symptoms WHERE LOWER(name) IN ({placeholders});", clean_inputs)
    resolved_sym_rows = cursor.fetchall()
    
    # Fallback substring matching if direct match misses
    if not resolved_sym_rows:
        like_clauses = " OR ".join(["LOWER(name) LIKE ?"] * len(clean_inputs))
        cursor.execute(f"SELECT id, name FROM symptoms WHERE {like_clauses};", [f"%{s}%" for s in clean_inputs])
        resolved_sym_rows = cursor.fetchall()

    if not resolved_sym_rows:
        return DiseasePredictResponse(input_symptoms=clean_inputs, total_matches_found=0, top_diseases=[])

    input_sym_id_map = {row[0]: row[1] for row in resolved_sym_rows}
    input_sym_ids = set(input_sym_id_map.keys())
    input_sym_names_set = set(row[1].title() for row in resolved_sym_rows)

    # 2. Fetch all diseases associated with at least one reported symptom
    sym_id_placeholders = ",".join(["?"] * len(input_sym_ids))
    cursor.execute(f"""
        SELECT DISTINCT d.id, d.name, d.severity_level, d.description
        FROM diseases d
        JOIN disease_symptoms ds ON d.id = ds.disease_id
        WHERE ds.symptom_id IN ({sym_id_placeholders});
    """, list(input_sym_ids))
    candidate_diseases = cursor.fetchall()

    predictions = []

    for d_id, d_name, d_sev, d_desc in candidate_diseases:
        # Fetch all symptoms for this disease
        cursor.execute("""
            SELECT s.id, s.name 
            FROM symptoms s
            JOIN disease_symptoms ds ON s.id = ds.symptom_id
            WHERE ds.disease_id = ?;
        """, (d_id,))
        disease_all_sym_rows = cursor.fetchall()
        
        disease_sym_names = [r[1].title() for r in disease_all_sym_rows]
        disease_sym_ids = set(r[0] for r in disease_all_sym_rows)

        # Calculate Matching vs Missing Symptoms
        matching_ids = input_sym_ids.intersection(disease_sym_ids)
        matching_symptoms = [input_sym_id_map[mid].title() for mid in matching_ids]

        missing_symptoms = [s_name for s_name in disease_sym_names if s_name.lower() not in [m.lower() for m in matching_symptoms]]

        # Calculate Confidence Score (0.0 to 1.0)
        sensitivity = len(matching_ids) / max(len(disease_sym_ids), 1)
        precision = len(matching_ids) / max(len(input_sym_ids), 1)
        confidence = round((sensitivity * 0.65) + (precision * 0.35), 2)
        conf_pct = round(confidence * 100.0, 1)

        # Fetch Precautions for disease
        cursor.execute("SELECT precaution FROM disease_precautions WHERE disease_id = ?;", (d_id,))
        precautions = [p_row[0] for p_row in cursor.fetchall()]

        predictions.append(PredictedDiseaseItem(
            disease_name=d_name,
            confidence=confidence,
            confidence_percentage=conf_pct,
            severity=d_sev or "Moderate",
            matching_symptoms=matching_symptoms,
            missing_symptoms=missing_symptoms,
            description=d_desc or "",
            precautions=precautions
        ))

    # Sort predictions by confidence descending
    predictions.sort(key=lambda x: x.confidence, reverse=True)
    top_predictions = predictions[:top_n]

    return DiseasePredictResponse(
        input_symptoms=clean_inputs,
        total_matches_found=len(predictions),
        top_diseases=top_predictions
    )
