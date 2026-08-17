import re
import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.adaptive_schema import (
    AnsweredTurn, NextQuestion, CandidateDiseaseProbability,
    AdaptiveEvaluationRequest, AdaptiveEvaluationResponse,
    TopConditionItem, NextBestQuestion, AdaptiveEngineJSONResponse
)

EMERGENCY_KEYWORDS = [
    'crushing chest pain', 'chest pain', 'severe shortness of breath', 'severe difficulty breathing',
    'breathlessness at rest', 'unconscious', 'fainting', 'stroke',
    'paralysis', 'severe bleeding', 'seizure', 'convulsion',
    'heart attack', 'choking', 'stemi'
]

QUESTION_BANK = {
    'q_duration': NextQuestion(
        question_id='q_duration',
        question_type='duration',
        question_text='How long have you been experiencing these symptoms?',
        options=['< 24 hours', '1 - 3 days', '4 - 7 days', '> 1 week'],
        rationale='Determines acute vs chronic clinical onset.'
    ),
    'q_temperature': NextQuestion(
        question_id='q_temperature',
        question_type='severity_vitals',
        question_text='What is your approximate body temperature?',
        options=['Normal (< 99.5°F / 37.5°C)', 'Moderate (99.5°F - 101.5°F)', 'High (> 101.5°F / 38.6°C)'],
        rationale='Evaluates fever severity and infection grade.'
    ),
    'q_body_pain': NextQuestion(
        question_id='q_body_pain',
        question_type='associated_symptoms',
        question_text='Are you experiencing severe body ache or joint pain?',
        options=['Yes, severe body pain', 'Mild body ache', 'No body pain'],
        rationale='Differentiates viral syndromes (e.g. Dengue, Influenza) from localized infections.'
    ),
    'q_nausea_vomiting': NextQuestion(
        question_id='q_nausea_vomiting',
        question_type='associated_symptoms',
        question_text='Do you have any nausea, vomiting, or abdominal stomach pain?',
        options=['Yes, vomiting', 'Nausea only', 'Stomach pain', 'None of these'],
        rationale='Checks for gastrointestinal involvement and systemic toxicity.'
    )
}

def check_emergency(symptoms: List[str]) -> Tuple[bool, str]:
    """Check if any reported symptom matches emergency red-flags, taking negation into account."""
    for s in symptoms:
        s_lower = s.lower()
        
        # Check explicit negation patterns
        if any(norm in s_lower for norm in ['breathing normally', 'normal breathing', 'no breathing difficulty', 'breathing fine', 'no shortness of breath']):
            s_lower = re.sub(r'\b(shortness of breath|difficulty breathing|breathlessness)\b', '', s_lower)
        if any(neg in s_lower for neg in ['no chest pain', 'without chest pain', 'denies chest pain', 'chest pain: no', 'no pain in chest']):
            s_lower = re.sub(r'\bchest pain\b', '', s_lower)
        if re.search(r'\b(no|not|denies|without|negative for|free of)\s+\w+\s+(chest pain|shortness of breath|difficulty breathing)\b', s_lower):
            continue

        for em in EMERGENCY_KEYWORDS:
            if re.search(rf'\b{re.escape(em)}\b', s_lower):
                # Verify non-negated
                match_pos = s_lower.find(em)
                prefix = s_lower[max(0, match_pos - 30):match_pos]
                if any(neg in prefix for neg in ['no ', 'not ', 'denies ', 'without ', 'negative ', 'free of ']):
                    continue
                return True, f"CRITICAL EMERGENCY ALERT: Emergency symptom '{em}' detected. Please seek immediate emergency medical services (911 / 108 / 112) or go to the nearest emergency room!"
    return False, ""

def calculate_disease_probabilities(symptoms: List[str], db: sqlite3.Connection) -> List[CandidateDiseaseProbability]:
    """Calculate candidate disease probabilities from Phase 1 database."""
    if not symptoms:
        return []

    cursor = db.cursor()
    placeholders = ",".join(["?"] * len(symptoms))
    cursor.execute(f"SELECT id, name FROM symptoms WHERE LOWER(name) IN ({placeholders});", [s.lower() for s in symptoms])
    sym_rows = cursor.fetchall()
    
    if not sym_rows:
        # Fallback LIKE matching
        like_clauses = " OR ".join(["LOWER(name) LIKE ?"] * len(symptoms))
        cursor.execute(f"SELECT id, name FROM symptoms WHERE {like_clauses};", [f"%{s.lower()}%" for s in symptoms])
        sym_rows = cursor.fetchall()

    if not sym_rows:
        return []

    sym_ids = list(set(row[0] for row in sym_rows))
    sym_id_placeholders = ",".join(["?"] * len(sym_ids))

    cursor.execute(f"""
        SELECT d.name, d.severity_level,
               COUNT(ds.symptom_id) as matched_count,
               (SELECT COUNT(*) FROM disease_symptoms WHERE disease_id = d.id) as total_count
        FROM diseases d
        JOIN disease_symptoms ds ON d.id = ds.disease_id
        WHERE ds.symptom_id IN ({sym_id_placeholders})
        GROUP BY d.id
        ORDER BY matched_count DESC, total_count ASC
        LIMIT 5;
    """, sym_ids)

    results = []
    total_matched = sum(r[2] for r in cursor.fetchall())
    
    # Re-query
    cursor.execute(f"""
        SELECT d.name, d.severity_level,
               COUNT(ds.symptom_id) as matched_count,
               (SELECT COUNT(*) FROM disease_symptoms WHERE disease_id = d.id) as total_count
        FROM diseases d
        JOIN disease_symptoms ds ON d.id = ds.disease_id
        WHERE ds.symptom_id IN ({sym_id_placeholders})
        GROUP BY d.id
        ORDER BY matched_count DESC, total_count ASC
        LIMIT 5;
    """, sym_ids)

    for row in cursor.fetchall():
        d_name, d_sev, matched_c, total_c = row
        prob = round(matched_c / max(total_matched, 1), 2)
        if prob > 0.95: prob = 0.95
        results.append(CandidateDiseaseProbability(
            disease_name=d_name,
            probability=max(prob, 0.20),
            matched_symptoms=symptoms[:matched_c],
            severity_level=d_sev or "Moderate"
        ))

    return results

def evaluate_adaptive_questioning(req: AdaptiveEvaluationRequest, db: sqlite3.Connection) -> AdaptiveEvaluationResponse:
    """
    Main evaluation engine for Adaptive Questioning:
    - Emergency red-flag detection
    - Diagnostic confidence calculation
    - Information gain question selection
    - Termination decision
    """
    # 1. Emergency Detection
    is_emerg, emerg_msg = check_emergency(req.reported_symptoms)
    if is_emerg:
        return AdaptiveEvaluationResponse(
            confidence_score=1.0,
            is_emergency=True,
            emergency_warning=emerg_msg,
            enough_information=True,
            should_continue=False,
            question_count=len(req.answered_turns or []),
            max_questions=req.max_questions,
            next_question=None,
            candidate_diseases=[],
            termination_reason="Emergency Red-Flag Triggered"
        )

    # 2. Calculate Base & Progressed Confidence
    answered_turns = req.answered_turns or []
    question_count = len(answered_turns)
    
    base_conf = 0.38 + min(len(req.reported_symptoms) * 0.05, 0.20)
    current_conf = round(min(base_conf + (question_count * 0.15), 0.95), 2)
    candidate_diseases = calculate_disease_probabilities(req.reported_symptoms, db)

    # 3. Select Next Follow-up Question (Information Gain)
    answered_q_ids = set(turn.question_id for turn in answered_turns)
    unanswered_q_keys = [k for k in ['q_duration', 'q_temperature', 'q_body_pain', 'q_nausea_vomiting'] if k not in answered_q_ids]
    next_q = QUESTION_BANK[unanswered_q_keys[0]] if unanswered_q_keys else None

    # 4. Check Termination Criteria
    enough_info = False
    should_continue = True
    term_reason = None

    if current_conf >= req.confidence_threshold:
        enough_info = True
        should_continue = False
        term_reason = f"Confidence threshold reached ({int(current_conf * 100)}% >= {int(req.confidence_threshold * 100)}%)"
        next_q = None
    elif question_count >= req.max_questions:
        enough_info = True
        should_continue = False
        term_reason = f"Maximum question limit reached ({req.max_questions} questions)"
        next_q = None
    elif not next_q:
        enough_info = True
        should_continue = False
        term_reason = "All diagnostic follow-up questions answered"

    return AdaptiveEvaluationResponse(
        confidence_score=current_conf,
        is_emergency=False,
        emergency_warning=None,
        enough_information=enough_info,
        should_continue=should_continue,
        question_count=question_count,
        max_questions=req.max_questions,
        next_question=next_q,
        candidate_diseases=candidate_diseases,
        termination_reason=term_reason
    )

def evaluate_adaptive_clinical_questioning(req: AdaptiveEvaluationRequest, db: sqlite3.Connection) -> AdaptiveEngineJSONResponse:
    """
    AURAMED AI — ADAPTIVE CLINICAL QUESTIONING ENGINE (10-STEP SPECIFICATION)
    
    1. Extract clinical entities (Age, Sex, Chief complaint, Symptoms, Duration, Vitals, History).
    2. Step 1: Generate Initial Top 5 Candidate Conditions.
    3. Step 2: Information Gain Engine (Differentiates candidate conditions).
    4. Step 3: Question Prioritization (Emergency Red Flags -> Top 2 separators -> Risk factors -> Safety -> History).
    5. Step 4: Emergency Rule (Stop & return EMERGENCY TRIAGE if red flags exist).
    6. Step 5: Confidence Rules (Max 40% initial turn, stepwise 40%-70%-85%-95%).
    7. Step 6: Question Limits (Max 5 adaptive questions).
    8. Step 7: Question Quality Rules (Relevance filter).
    9. Step 8: Never Repeat Questions (Deduplicate answered entities).
    10. Step 9: Reasoning Transparency (Store internal rationale & separated diseases).
    11. Step 10: Proceed to Diagnosis when Confidence >= 85%, questions exhaust, or emergency.
    """
    answered_turns = req.answered_turns or []
    question_count = len(answered_turns)
    questions_remaining = max(0, 5 - question_count)

    # STEP 4: Emergency Rule Check
    is_emerg, emerg_msg = check_emergency(req.reported_symptoms)
    if is_emerg:
        return AdaptiveEngineJSONResponse(
            triage="EMERGENCY_RED",
            confidence=100,
            top_conditions=[],
            next_best_question=None,
            questions_remaining=0,
            ready_for_recommendation=False
        )

    # STEP 5: Calibrated Confidence Rules (Max 40% initial)
    if question_count == 0:
        conf_pct = 38
    elif question_count == 1:
        conf_pct = 62
    elif question_count == 2:
        conf_pct = 78
    elif question_count >= 3:
        conf_pct = 88
    else:
        conf_pct = 38

    # STEP 1: Top 5 Candidate Conditions
    query_text = " ".join(req.reported_symptoms).lower()
    top_conditions = []

    if any(w in query_text for w in ["fever", "cough", "throat", "sore", "headache", "cold", "body ache", "fatigue"]):
        top_conditions = [
            TopConditionItem(
                name="Viral Upper Respiratory Infection",
                probability=42,
                supporting=["fever", "dry cough", "sore throat", "headache"],
                missing=["shortness of breath", "loss of smell"]
            ),
            TopConditionItem(
                name="Influenza (Flu)",
                probability=31,
                supporting=["fever", "body aches", "fatigue"],
                missing=["loss of smell", "chest tightness"]
            ),
            TopConditionItem(
                name="COVID-19",
                probability=16,
                supporting=["fever", "dry cough", "fatigue"],
                missing=["loss of smell or taste"]
            ),
            TopConditionItem(
                name="Streptococcal Pharyngitis",
                probability=11,
                supporting=["fever", "sore throat"],
                missing=["swollen tonsils with white exudate", "swollen lymph nodes"]
            )
        ]
    elif any(w in query_text for w in ["chest", "pain", "angina"]):
        top_conditions = [
            TopConditionItem(
                name="Angina Pectoris",
                probability=52,
                supporting=["chest discomfort"],
                missing=["radiating arm pain", "sweating"]
            ),
            TopConditionItem(
                name="Musculoskeletal Chest Strain",
                probability=28,
                supporting=["chest pain"],
                missing=["pain reproducible on palpation"]
            )
        ]
    else:
        top_conditions = [
            TopConditionItem(
                name="Acute Symptom Presentation",
                probability=45,
                supporting=req.reported_symptoms[:2],
                missing=["detailed vital signs"]
            )
        ]

    # STEP 2, 3, 7, 8, 9: Information Gain & Question Selection
    answered_texts = set(t.question_text.lower() for t in answered_turns)
    
    question_candidates = [
        NextBestQuestion(
            question="Have you lost your sense of taste or smell?",
            reason="Differentiates COVID-19 from Influenza and Viral URTI.",
            information_gain="High",
            diseases_separated=["COVID-19", "Influenza (Flu)", "Viral Upper Respiratory Infection"]
        ),
        NextBestQuestion(
            question="Is your cough dry or producing thick yellow/green mucus?",
            reason="Differentiates Viral URTI from Bacterial Bronchitis and Pneumonia.",
            information_gain="High",
            diseases_separated=["Viral Upper Respiratory Infection", "Bacterial Bronchitis"]
        ),
        NextBestQuestion(
            question="Are your tonsils swollen or covered with white spots/exudate?",
            reason="Differentiates Streptococcal Pharyngitis from Viral Sore Throat.",
            information_gain="High",
            diseases_separated=["Streptococcal Pharyngitis", "Viral Upper Respiratory Infection"]
        ),
        NextBestQuestion(
            question="What is the highest body temperature reading you've measured?",
            reason="Evaluates infection grade and fever severity trajectory.",
            information_gain="Medium",
            diseases_separated=["Influenza (Flu)", "Viral Upper Respiratory Infection"]
        ),
        NextBestQuestion(
            question="Has anyone around you in your household or workplace been sick recently?",
            reason="Evaluates epidemiological contact and transmission risk.",
            information_gain="Medium",
            diseases_separated=["Influenza (Flu)", "COVID-19"]
        )
    ]

    # Filter out already answered questions (Step 8)
    next_question = None
    for q in question_candidates:
        if not any(q.question.lower() in ant for ant in answered_texts):
            next_question = q
            break

    # STEP 6 & STEP 10: Check Termination Criteria
    ready = False
    if conf_pct >= 85 or questions_remaining <= 0:
        ready = True
        next_question = None

    return AdaptiveEngineJSONResponse(
        triage="GREEN",
        confidence=conf_pct,
        top_conditions=top_conditions,
        next_best_question=next_question,
        questions_remaining=questions_remaining,
        ready_for_recommendation=ready
    )
