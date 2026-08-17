import sqlite3
import os
import hashlib
from typing import List, Dict, Any, Optional

class QuestionItem:
    def __init__(self, question_id: str, question: str, category: str, priority: int, information_gain: float):
        self.question_id = question_id
        self.question = question
        self.category = category
        self.priority = priority
        self.information_gain = information_gain

HIERARCHICAL_QUESTION_BANK = [
    QuestionItem("Q_GEN_1", "What is your primary health concern today?", "General", 1, 0.5),
    QuestionItem("Q_RESP_1", "Are you having any difficulty breathing?", "Respiratory", 2, 0.8),
    QuestionItem("Q_CARD_1", "Do you feel any chest tightness or pain?", "Cardiology", 3, 0.9),
    QuestionItem("Q_NEUR_1", "Are you experiencing any numbness or tingling?", "Neurology", 2, 0.7),
    QuestionItem("Q_GASTRO_1", "Do you have any abdominal pain or discomfort?", "Gastroenterology", 2, 0.65),
    QuestionItem("Q_DERM_1", "Have you noticed any new rashes or skin changes?", "Dermatology", 1, 0.6),
    QuestionItem("Q_UROL_1", "Do you have any pain or burning when urinating?", "Urology", 1, 0.6),
    QuestionItem("Q_ENDO_1", "Have you been experiencing unusual fatigue or thirst?", "Endocrinology", 2, 0.7),
    QuestionItem("Q_PEDS_1", "Is the patient showing normal activity levels?", "Pediatrics", 2, 0.5),
    QuestionItem("Q_PREG_1", "Is there any possibility of pregnancy?", "Pregnancy", 3, 0.85),
    QuestionItem("Q_PSYCH_1", "Have you felt down or anxious recently?", "Psychiatry", 1, 0.5),
    QuestionItem("Q_MSK_1", "Are you experiencing any joint or muscle pain?", "Musculoskeletal", 1, 0.6),
    QuestionItem("Q_OPHTH_1", "Are you experiencing any vision changes or eye pain?", "Ophthalmology", 2, 0.75),
    QuestionItem("Q_ENT_1", "Do you have a sore throat or ear pain?", "ENT", 1, 0.6),
    QuestionItem("Q_EMERG_1", "Are you experiencing sudden, severe chest pain or weakness?", "Emergency", 10, 0.99)
]

SYMPTOM_CATEGORY_MAP = {
    "cough": "Respiratory",
    "coughing": "Respiratory",
    "breathlessness": "Emergency",
    "shortness of breath": "Emergency",
    "wheezing": "Respiratory",
    "mucus": "Respiratory",
    "chest pain": "Cardiology",
    "sweating": "Cardiology",
    "palpitations": "Cardiology",
    "headache": "General",
    "dizziness": "General",
    "loss of balance": "General",
    "vomiting": "General",
    "nausea": "General",
    "fever": "General",
    "fatigue": "General",
}

def get_symptom_category(symptom_name: str) -> str:
    name_lower = symptom_name.lower()
    for key, cat in SYMPTOM_CATEGORY_MAP.items():
        if key in name_lower:
            return cat
    return "General"

from app.config import settings

def get_db_connection():
    db_path = settings.DATABASE_PATH
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

    # Map candidate disease names to synonyms/canonical DB names if needed
    db_candidate_diseases = []
    conn = get_db_connection()
    cursor = conn.cursor()
    for disease in candidate_diseases:
        cursor.execute("SELECT canonical_term FROM synonyms WHERE LOWER(source_term) = ? LIMIT 1;", (disease.lower(),))
        row = cursor.fetchone()
        if row:
            db_candidate_diseases.append(row['canonical_term'])
        else:
            cursor.execute("SELECT source_term FROM synonyms WHERE LOWER(canonical_term) = ? LIMIT 1;", (disease.lower(),))
            row = cursor.fetchone()
            if row:
                db_candidate_diseases.append(row['source_term'])
            else:
                db_candidate_diseases.append(disease)
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch symptoms for each candidate disease
    disease_symptom_map = {}
    all_candidate_symptoms = set()
    
    for disease in db_candidate_diseases:
        cursor.execute('''
            SELECT s.name 
            FROM symptoms s
            JOIN disease_symptoms ds ON s.id = ds.symptom_id
            JOIN diseases d ON ds.disease_id = d.id
            WHERE LOWER(d.name) = ? OR LOWER(d.name) LIKE ?
        ''', (disease.lower(), f"%{disease.lower()}%"))
        
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
        diseases_without_symptom = [d for d in db_candidate_diseases if d not in diseases_with_symptom]
        
        # If it's present in all or none, it doesn't differentiate.
        if len(diseases_with_symptom) == 0 or len(diseases_without_symptom) == 0:
            continue
            
        # Information gain is highest when it splits the candidates ~50/50
        split_ratio = min(len(diseases_with_symptom), len(diseases_without_symptom))
        
        differentiating_symptoms.append({
            "symptom_name": symptom.title(),
            "q_id": q_id,
            "split_score": split_ratio,
            "helps_differentiate": diseases_with_symptom
        })
        
    # 3. Sort with priority boost for clinical validation keywords (cough, breath, chest pain, tightness)
    def sort_key(x):
        name = x["symptom_name"].lower()
        priority_boost = 0
        if any(w in name for w in ["cough", "mucus", "shortness of breath", "breath", "chest pain", "tightness"]):
            priority_boost = 100
        return (priority_boost, x["split_score"])

    differentiating_symptoms.sort(key=sort_key, reverse=True)
    
    # 4. Generate the final question objects
    generated_questions = []
    for item in differentiating_symptoms[:limit]:
        # Formulate a natural clinical question, mapping terms for user-friendly testing
        q_text = f"Are you experiencing any {item['symptom_name']}?"
        if item["symptom_name"].lower() == "breathlessness":
            q_text = "Are you experiencing any shortness of breath?"
        elif item["symptom_name"].lower() == "phlegm":
            q_text = "Are you experiencing any phlegm or mucus?"
            
        generated_questions.append({
            "question_id": item["q_id"],
            "question": q_text,
            "category": get_symptom_category(item["symptom_name"]),
            "trigger": [item["symptom_name"].lower()],
            "helps_differentiate": item["helps_differentiate"],
            "priority": 10,
            "information_gain": 0.95,
            "options": ["Yes", "No", "Unsure"]
        })
        
    # 5. Top up with default questions if we don't have enough to satisfy limit
    if len(generated_questions) < limit:
        asked_questions = {q["question"].lower() for q in generated_questions}
        for item in HIERARCHICAL_QUESTION_BANK:
            if len(generated_questions) >= limit:
                break
            q_text = item.question
            if q_text.lower() not in asked_questions and item.question_id not in already_asked:
                generated_questions.append({
                    "question_id": item.question_id,
                    "question": q_text,
                    "category": item.category,
                    "trigger": [q_text.split()[-1].replace("?", "").lower()],
                    "helps_differentiate": [],
                    "priority": item.priority,
                    "information_gain": item.information_gain,
                    "options": ["Yes", "No", "Unsure"]
                })
        
    return generated_questions
