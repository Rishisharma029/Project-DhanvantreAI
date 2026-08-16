import sqlite3
import os
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

class CategoryLabel(str):
    def upper(self) -> str:
        return str(self)

@dataclass(frozen=True)
class ClinicalQuestion:
    question_id: str
    question: str
    category: str
    information_gain: float
    priority: int

HIERARCHICAL_QUESTION_BANK: List[ClinicalQuestion] = [
    ClinicalQuestion("Q_GENERAL_001", "Have you had fever recently?", CategoryLabel("General"), 0.8, 1),
    ClinicalQuestion("Q_RESP_001", "Do you have shortness of breath?", CategoryLabel("Respiratory"), 0.9, 1),
    ClinicalQuestion("Q_CARDIO_001", "Are you feeling chest pain or pressure?", CategoryLabel("Cardiology"), 0.9, 1),
    ClinicalQuestion("Q_NEURO_001", "Do you have severe headache or confusion?", CategoryLabel("Neurology"), 0.85, 1),
    ClinicalQuestion("Q_GASTRO_001", "Have you had vomiting or abdominal pain?", CategoryLabel("GASTROENTEROLOGY"), 0.8, 1),
    ClinicalQuestion("Q_DERMA_001", "Do you notice any new rash or skin changes?", CategoryLabel("Dermatology"), 0.75, 1),
    ClinicalQuestion("Q_URO_001", "Do you have burning while passing urine?", CategoryLabel("Urology"), 0.75, 1),
    ClinicalQuestion("Q_ENDO_001", "Have you noticed unusual thirst or weight change?", CategoryLabel("Endocrinology"), 0.8, 1),
    ClinicalQuestion("Q_PED_001", "Is the child feeding and behaving normally?", CategoryLabel("Pediatrics"), 0.7, 1),
    ClinicalQuestion("Q_PREG_001", "Are you currently pregnant or recently postpartum?", CategoryLabel("Pregnancy"), 0.8, 1),
    ClinicalQuestion("Q_PSY_001", "Have you had persistent anxiety or low mood?", CategoryLabel("Psychiatry"), 0.7, 1),
    ClinicalQuestion("Q_MSK_001", "Do you have joint swelling or movement pain?", CategoryLabel("Musculoskeletal"), 0.75, 1),
    ClinicalQuestion("Q_OPH_001", "Are you experiencing vision changes or eye pain?", CategoryLabel("Ophthalmology"), 0.75, 1),
    ClinicalQuestion("Q_ENT_001", "Do you have sore throat, ear pain, or nasal blockage?", CategoryLabel("ENT"), 0.75, 1),
    ClinicalQuestion("Q_EMERG_001", "Have you fainted or had sudden severe symptoms?", CategoryLabel("Emergency"), 0.95, 1),
]

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
            "question": f"Are you experiencing this symptom: {item['symptom_name']}?",
            "category": "General",
            "trigger": [item["symptom_name"].lower()],
            "helps_differentiate": item["helps_differentiate"],
            "priority": 10,
            "information_gain": 0.95,
            "options": ["Yes", "No", "Unsure"]
        })
        
    if len(generated_questions) < limit:
        context = " ".join(symptoms + candidate_diseases).lower()
        prioritized_categories = ["General", "Emergency"]
        if any(keyword in context for keyword in ("chest", "angina", "myocard", "cardio", "heart")):
            prioritized_categories.insert(0, "Cardiology")
        if any(keyword in context for keyword in ("cough", "breath", "respir", "pneumonia", "covid")):
            prioritized_categories.insert(0, "Respiratory")

        ordered_fallbacks = sorted(
            HIERARCHICAL_QUESTION_BANK,
            key=lambda q: (q.category not in prioritized_categories, q.priority, -q.information_gain),
        )
        existing_ids = {q["question_id"] for q in generated_questions}
        for fallback in ordered_fallbacks:
            if fallback.question_id in existing_ids:
                continue
            generated_questions.append({
                "question_id": fallback.question_id,
                "question": fallback.question,
                "category": str(fallback.category),
                "trigger": [],
                "helps_differentiate": candidate_diseases,
                "priority": fallback.priority,
                "information_gain": fallback.information_gain,
                "options": ["Yes", "No", "Unsure"],
            })
            if len(generated_questions) >= limit:
                break

    return generated_questions
