import sqlite3
import os
import hashlib
from typing import List, Dict, Any, Optional

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "medical_database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def _generate_question_id(symptom_name: str) -> str:
    """Generate a deterministic ID for a symptom question."""
    hash_object = hashlib.md5(symptom_name.encode())
    return f"Q_{hash_object.hexdigest()[:8]}"

def rank_questions_by_information_gain(
    symptoms: List[str],
    candidate_diseases: List[str],
    already_asked_ids: List[str] = None,
    limit: int = 3,
    patient_age: Optional[int] = None,
    patient_gender: Optional[str] = None,
    is_pregnant: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """
    Dynamically generates and ranks follow-up questions to differentiate between the top candidate diseases.
    Uses set theory against the medical_database.db to find highly distinguishing symptoms.
    """
    already_asked = set(already_asked_ids or [])
    reported_symptoms_lower = {s.lower() for s in symptoms}
    
    if not candidate_diseases or len(candidate_diseases) < 2:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch symptoms for each candidate disease
    disease_symptom_map = {}
    all_candidate_symptoms = set()
    
    for disease in candidate_diseases:
        cursor.execute('''
            SELECT s.name 
            FROM symptoms s
            JOIN disease_symptoms ds ON s.id = ds.symptom_id
            JOIN diseases d ON ds.disease_id = d.id
            WHERE d.name = ?
        ''', (disease,))
        
        disease_symptoms = {row['name'].lower() for row in cursor.fetchall()}
        disease_symptom_map[disease] = disease_symptoms
        all_candidate_symptoms.update(disease_symptoms)

    conn.close()

    # 2. Find highly differentiating symptoms (present in some, but not all candidates)
    # We want symptoms that split the candidate list as evenly as possible.
    differentiating_symptoms = []
    
    for symptom in all_candidate_symptoms:
        # Skip if patient already reported it
        if symptom in reported_symptoms_lower:
            continue
            
        # Skip if we already asked about this symptom
        q_id = _generate_question_id(symptom)
        if q_id in already_asked:
            continue
            
        # Calculate how many diseases have this symptom
        diseases_with_symptom = [d for d, syms in disease_symptom_map.items() if symptom in syms]
        diseases_without_symptom = [d for d in candidate_diseases if d not in diseases_with_symptom]
        
        # If it's present in all or none, it doesn't differentiate.
        if len(diseases_with_symptom) == 0 or len(diseases_without_symptom) == 0:
            continue
            
        # Information gain is highest when it splits the candidates ~50/50
        # We'll score by closeness to a 50/50 split (e.g., 1 vs 1 in a 2-disease list, or 1 vs 2 in a 3-disease list)
        split_ratio = min(len(diseases_with_symptom), len(diseases_without_symptom))
        
        differentiating_symptoms.append({
            "symptom_name": symptom.title(),
            "q_id": q_id,
            "split_score": split_ratio,
            "helps_differentiate": diseases_with_symptom
        })
        
    # 3. Sort by split_score (descending) to maximize information gain
    differentiating_symptoms.sort(key=lambda x: x["split_score"], reverse=True)
    
    # 4. Generate the final question objects
    generated_questions = []
    for item in differentiating_symptoms[:limit]:
        # Formulate a natural clinical question
        generated_questions.append({
            "question_id": item["q_id"],
            "question": f"Are you experiencing any {item['symptom_name']}?",
            "category": "Dynamic Differentiation",
            "trigger": [item["symptom_name"].lower()],
            "helps_differentiate": item["helps_differentiate"],
            "priority": 10,
            "information_gain": 0.95,
            "options": ["Yes", "No", "Unsure"]
        })
        
    return generated_questions
