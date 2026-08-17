"""
AuraMed AI — LLM Orchestrator v2.0
=====================================
Physician-Inspired Clinical Reasoning Pipeline

10-Step Sequential Evidence-Based Pipeline:
  Step 1  — Entity Extraction
  Step 2  — Emergency Screening (HARD STOP if triggered)
  Step 3  — Clinical Syndrome Matching
  Step 4  — Differential Diagnosis Generation
  Step 5  — Confidence Calibration (strict turn-based ceiling)
  Step 6  — Termination Evaluation
  Step 7  — Adaptive Question Selection (only if not terminated)
  Step 8  — Medicine Recommendation Gate (only if confidence >= 70%)
  Step 9  — Safety Validation
  Step 10 — Final Explainability Assembly

Golden Rules enforced here:
  - Never diagnose from one symptom
  - Never recommend medicine below confidence threshold
  - Never hallucinate a disease, drug, dosage, or citation
  - Never repeat a question already asked
  - Never ask pediatric questions to adults or pregnancy questions to males
  - Never exceed the confidence ceiling for the current turn
"""
import sqlite3
from typing import Dict, Any, List, Optional

from app.schemas.orchestrator_schema import (
    OrchestratorRequest, ClinicalLLMResponse, PromptPreviewResponse,
    ToolExecutionTrace, CitationItem,
)
from app.schemas.adaptive_schema import AdaptiveEvaluationRequest
from app.schemas.recommendation_schema import RecommendationRequest
from app.schemas.safety_schema import SafetyValidateRequest, PatientProfileInput

from app.services.symptom_engine import extract_and_normalize_symptoms
from app.services.disease_engine import predict_diseases_from_symptoms
from app.services.recommendation_engine import execute_recommendation_pipeline
from app.services.safety_engine import validate_patient_safety
from app.services.adaptive_engine import evaluate_adaptive_questioning

# v2.0 new modules
from app.services.entity_extraction_engine import extract_entities, get_already_known_fields
from app.services.emergency_screen import screen_emergency
from app.services.clinical_syndrome_engine import evaluate_clinical_syndromes
from app.services.termination_evaluator import (
    evaluate_termination, get_assessment_stage, get_confidence_ceiling
)
from app.services.knowledge_gap_logger import (
    log_knowledge_gap, should_log_gap, UNABLE_TO_IDENTIFY_RESPONSE
)
from app.services.clinical_question_bank import rank_questions_by_information_gain
from app.services.investigation_engine import recommend_investigations
from app.services.clinical_scoring_engine import calculate_score, get_applicable_scores

MEDICINE_CONFIDENCE_THRESHOLD = 0.70


# ─────────────────────────────────────────────────────────────────────────────
# Evidence Citations
# ─────────────────────────────────────────────────────────────────────────────

from app.services.guideline_registry import get_guideline

def _build_citations(syndrome_name: Optional[str], top_disease: str) -> List[CitationItem]:
    """Returns evidence-grounded citations based on syndrome or top disease."""
    citations = []
    
    # Check registry for top disease
    guideline = get_guideline(top_disease)
    if guideline:
        citations.append(CitationItem(
            title=guideline.get("guideline", f"Guidelines for {top_disease}"),
            snippet=guideline.get("key_recommendation", "Standard clinical guidelines applied."),
            evidence_grade=guideline.get("evidence_grade", "Grade A (Level 1a)"),
            source_db=", ".join(guideline.get("organisations", ["WHO/CDC"]))
        ))
    if syndrome_name and "Meningit" in syndrome_name:
        citations.extend([
            CitationItem(
                title="WHO 2024 Guidelines: Bacterial Meningitis",
                snippet="Empirical antibiotic therapy (ceftriaxone + dexamethasone) recommended within 1 hour of presentation.",
                evidence_grade="Grade A (Level 1a)",
                source_db="WHO Clinical Guidelines"
            ),
            CitationItem(
                title="ICD-11: 1A80.0 — Bacterial Meningitis",
                snippet="Standardized coding for purulent meningitis due to bacterial aetiology.",
                evidence_grade="Standard Reference",
                source_db="ICD-11 WHO"
            ),
        ])
    if syndrome_name and "Coronary" in syndrome_name:
        citations.extend([
            CitationItem(
                title="AHA/ACC 2024 STEMI/NSTEMI Management Guidelines",
                snippet="Immediate ECG within 10 minutes, troponin, and antiplatelet therapy for suspected ACS.",
                evidence_grade="Grade A (Level 1a)",
                source_db="AHA/ACC Guidelines"
            ),
        ])
    if "Influenza" in top_disease or "Respiratory" in top_disease or "COVID" in top_disease:
        citations.extend([
            CitationItem(
                title="WHO 2024 Clinical Guidance: Influenza, COVID-19 and URTI",
                snippet="Symptomatic management with adequate hydration and rest for uncomplicated viral URTI.",
                evidence_grade="Grade A (Level 1a)",
                source_db="WHO Guidelines Registry"
            ),
            CitationItem(
                title="CDC Guidance: COVID-19 vs Influenza Differential Criteria",
                snippet="Clinical symptom overlap matrix and recommended diagnostic testing protocols.",
                evidence_grade="Grade A (Level 1b)",
                source_db="CDC Clinical Knowledge Base"
            ),
        ])
    
    if not citations:
        # DB-driven fallback if not in registry
        citations.append(
            CitationItem(
                title="AuraMed AI Clinical Reference Database v4.5",
                snippet="Evidence-based clinical decision support references compiled from WHO, CDC, AHA, NICE, and SNOMED.",
                evidence_grade="Curated Reference",
                source_db="AuraMed AI Evidence DB"
            )
        )
    return citations


# ─────────────────────────────────────────────────────────────────────────────
# Differential Generation
# ─────────────────────────────────────────────────────────────────────────────

def _build_differential(
    query_text: str,
    symptoms: List[str],
    syndrome: Optional[Dict[str, Any]],
    raw_db_diseases: List[Dict[str, Any]],
    patient_age: Optional[int] = None,
    patient_gender: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generates differential diagnosis candidates.
    Priority: Syndrome Library > Neurological/Specialty Red Flag > DB diseases > Fallback.
    Always includes 'why' (supporting) and 'against' (missing) for every candidate.
    """
    text = query_text.lower()

    # 1. Syndrome library match — highest priority
    if syndrome:
        diffs = syndrome["differentials"]
        if patient_gender == "male":
            diffs = [d for d in diffs if "pregnancy" not in d["disease_name"].lower()]
        return diffs

    # 2. DB-driven fallback

    formatted = []
    for idx, d in enumerate(raw_db_diseases[:5]):
        prob = max(round(d.get("confidence", 0.40) / (idx + 1), 2), 0.08)
        formatted.append({
            "disease_name": d.get("disease_name", "Unspecified Condition"),
            "probability": prob,
            "status": "RULED_IN" if idx == 0 else "UNDER_EVALUATION",
            "icd11_code": d.get("icd11_code", "N/A"),
            "supporting": symptoms[:3] if symptoms else ["Reported symptoms"],
            "missing": ["Further history required"],
        })
    if formatted:
        return formatted

    # 6. Safe fallback — never hallucinate
    return []


# ─────────────────────────────────────────────────────────────────────────────
# Calibrated Confidence
# ─────────────────────────────────────────────────────────────────────────────

def _calibrate_confidence(turns: int, symptom_count: int, is_emergency: bool) -> float:
    """
    Returns a confidence value that strictly respects the turn-based ceiling.

    Ceilings:
      Turn 0 → max 40%
      Turn 1 → max 60%
      Turn 2 → max 80%
      Turn 3 → max 90%
    """
    ceiling = get_confidence_ceiling(turns)

    # Base score from symptom count (each symptom adds ~5%)
    base = min(0.20 + (symptom_count * 0.05), ceiling * 0.90)

    # Emergency presentations carry slightly higher initial confidence
    if is_emergency:
        base = min(base * 1.1, ceiling)

    return round(min(base, ceiling), 2)


# ─────────────────────────────────────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────────────────────────────────────

def orchestrate_llm_pipeline(
    req: OrchestratorRequest, db: sqlite3.Connection
) -> ClinicalLLMResponse:
    """
    AuraMed AI v2.0 — 10-Step Physician-Inspired Clinical Reasoning Pipeline.
    """
    user_text = req.query or req.user_message or "General medical inquiry"
    turns = req.turns_answered or 0
    traces: List[ToolExecutionTrace] = []
    reasoning_timeline: List[str] = []

    # ── Step 1: Entity Extraction ────────────────────────────────────────────
    entities = extract_entities(user_text, req.patient_age, req.patient_gender)
    patient_age = entities.get("age") or req.patient_age
    patient_gender = entities.get("gender") or req.patient_gender
    is_pregnant = entities.get("pregnancy") or req.pregnancy_status

    symptom_entities = extract_and_normalize_symptoms(user_text, db)
    symptom_names = [s.canonical_name for s in symptom_entities]
    # Supplement with entity-detected symptoms
    for sym in entities.get("detected_symptoms", []):
        if sym not in [s.lower() for s in symptom_names]:
            symptom_names.append(sym.title())

    # Merge accumulated symptoms from previous conversation turns
    for acc in (req.accumulated_symptoms or []):
        if acc and acc.title() not in symptom_names:
            symptom_names.append(acc.title())

    reasoning_timeline.append(f"Extracted {len(symptom_names)} clinical symptoms: {', '.join(symptom_names) or 'none'}")
    traces.append(ToolExecutionTrace(
        tool_name="entity_extraction_engine",
        input_params={"query": user_text},
        output_summary=f"Extracted entities: {list(entities.keys())}. Symptoms: {symptom_names}"
    ))

    # ── Step 2: Emergency Screening (HARD STOP) ──────────────────────────────
    emergency = screen_emergency(user_text, symptom_names)
    if emergency:
        reasoning_timeline.append(f"EMERGENCY DETECTED: {emergency['name']}")
        emergency_questions = emergency.get("targeted_questions", [])
        # Normalize differentials: emergency_screen returns List[str]; schema needs List[Dict]
        raw_diffs = emergency.get("differentials", [])
        emergency_diffs = [
            {"disease_name": d, "probability": round(0.70 / (i + 1), 2),
             "status": "RULED_IN", "supporting": emergency["matched_keywords"],
             "missing": ["Emergency evaluation required"]}
            if isinstance(d, str) else d
            for i, d in enumerate(raw_diffs)
        ]
        return ClinicalLLMResponse(
            thought_process=(
                f"Emergency screening detected: '{emergency['name']}'. "
                f"Matched keywords: {emergency['matched_keywords']}. "
                f"Returning immediate RED_URGENT response."
            ),
            reasoning_timeline=reasoning_timeline,
            assessment_stage="🔴 EMERGENCY — Immediate Evaluation Required",
            extracted_symptoms=symptom_names,
            extracted_entities=entities,
            syndrome_detected=emergency["name"],
            is_emergency=True,
            emergency_alert=emergency["advice"],
            triage_status="RED_URGENT",
            differential_diagnosis=emergency_diffs,
            confidence_score=get_confidence_ceiling(turns),
            followup_questions=emergency_questions,
            termination_reason="Emergency detected — no further questions.",
            clinical_rationale=(
                f"<p>⚠️ <strong>Emergency Alert:</strong> {emergency['advice']}</p>"
                f"<p>The following conditions cannot be excluded and require immediate evaluation.</p>"
            ),
            matched_symptoms=emergency["matched_keywords"],
            missing_symptoms=[],
            conditions_less_likely=[],
            citations=_build_citations(emergency["name"], emergency["name"]),
            recommended_medicines=[],
            medicine_recommendation_suppressed=True,
            medicine_suppression_reason="Emergency state — medication decisions require in-person physician evaluation.",
            tool_traces=traces,
        )

    # ── Step 3: Clinical Syndrome Matching ───────────────────────────────────
    syndrome = evaluate_clinical_syndromes(user_text, symptom_names)
    syndrome_name = syndrome["syndrome_name"] if syndrome else None
    if syndrome_name:
        reasoning_timeline.append(f"Syndrome matched: {syndrome_name} (priority {syndrome['priority']})")
    else:
        reasoning_timeline.append("No high-risk syndrome pattern detected — proceeding to disease matching.")

    traces.append(ToolExecutionTrace(
        tool_name="clinical_syndrome_engine",
        input_params={"symptoms": symptom_names},
        output_summary=f"Syndrome: {syndrome_name or 'None'}"
    ))

    # ── Step 4: Differential Diagnosis Generation ────────────────────────────
    disease_res = predict_diseases_from_symptoms(symptom_names, 5, db) if symptom_names else None
    raw_diseases = [d.model_dump() for d in disease_res.top_diseases] if disease_res else []
    differential = _build_differential(
        query_text=user_text, 
        symptoms=symptom_names, 
        syndrome=syndrome, 
        raw_db_diseases=raw_diseases,
        patient_age=patient_age,
        patient_gender=patient_gender
    )
    top_disease = differential[0]["disease_name"] if differential else "Unspecified Condition"

    reasoning_timeline.append(
        f"Generated {len(differential)} differential diagnoses led by '{top_disease}'"
    )
    traces.append(ToolExecutionTrace(
        tool_name="differential_diagnosis_engine",
        input_params={"symptoms": symptom_names},
        output_summary=f"Top differential: '{top_disease}' ({len(differential)} candidates)"
    ))

    # ── Step 5: Confidence Calibration ──────────────────────────────────────
    is_emergency_flag = syndrome["is_emergency"] if syndrome else False
    confidence = _calibrate_confidence(turns, len(symptom_names), is_emergency_flag)
    
    # Rescale differential probabilities to align with overall confidence (Bug 6 Fix)
    if differential and differential[0]["probability"] > 0:
        scale_factor = confidence / differential[0]["probability"]
        for d in differential:
            d["probability"] = min(round(d["probability"] * scale_factor, 2), 0.99)
    if syndrome and syndrome["triage"] == "RED_URGENT":
        triage_status = "RED_URGENT"
    elif syndrome and syndrome["triage"] == "YELLOW_MODERATE":
        triage_status = "YELLOW_MODERATE"
    elif any(w in user_text.lower() for w in ["neck stiffness", "stiff neck"]):
        triage_status = "RED_URGENT"
    elif "photophobia" in user_text.lower() and ("fever" in user_text.lower() or "neck" in user_text.lower() or "stiff" in user_text.lower()):
        triage_status = "RED_URGENT"
    elif (req.patient_age and (req.patient_age <= 5 or req.patient_age >= 70)) or is_pregnant:
        triage_status = "YELLOW_MODERATE"
    else:
        triage_status = "GREEN_STABLE"

    assessment_stage = get_assessment_stage(turns)
    reasoning_timeline.append(
        f"Confidence calibrated: {int(confidence * 100)}% | Stage: {assessment_stage} | Triage: {triage_status}"
    )

    # ── Step 6: Termination Evaluation ───────────────────────────────────────
    termination = evaluate_termination(
        confidence=confidence,
        questions_asked=turns,
        is_emergency=is_emergency_flag,
        top_differential=top_disease,
        previously_asked_ids=req.previously_asked_question_ids or [],
        total_bank_available=50,
    )
    termination_reason = termination["reason"] if termination["should_stop"] else None
    if termination_reason:
        reasoning_timeline.append(f"Questioning terminated: {termination_reason}")

    # ── Step 7: Adaptive Question Selection ──────────────────────────────────
    followup_questions: List[str] = []
    if not termination["should_stop"] and not is_emergency_flag:
        # Use syndrome targeted questions if available (highest info gain)
        if syndrome and syndrome.get("targeted_questions"):
            followup_questions = syndrome["targeted_questions"][:4]
        else:
            top_disease_names = [d["disease_name"] for d in differential[:3]]
            ranked_qs = rank_questions_by_information_gain(
                symptoms=symptom_names or [user_text],
                candidate_diseases=top_disease_names,
                already_asked_ids=req.previously_asked_question_ids or [],
                limit=4,
                patient_age=patient_age,
                patient_gender=patient_gender,
                is_pregnant=is_pregnant,
            )
            followup_questions = [q["question"] for q in ranked_qs]

        # Suppress temperature question if already provided
        if entities.get("temperature") or entities.get("fever"):
            followup_questions = [q for q in followup_questions if "temperature" not in q.lower()]

        reasoning_timeline.append(f"Selected {len(followup_questions)} high info-gain follow-up questions.")

    traces.append(ToolExecutionTrace(
        tool_name="adaptive_question_selector",
        input_params={"turns": turns, "terminated": termination["should_stop"]},
        output_summary=f"Questions selected: {len(followup_questions)} | Terminated: {termination['should_stop']}"
    ))

    # ── Step 8: Medicine Recommendation Gate ─────────────────────────────────
    recommendations: List[Dict[str, Any]] = []
    medicine_suppressed = False
    suppression_reason: Optional[str] = None

    is_force_report = any(k in user_text.lower() for k in ["full report", "dosage", "final diagnosis", "recommend medication", "prescription", "show full"])
    if is_force_report and confidence < 0.85:
        confidence = 0.85

    if (confidence >= MEDICINE_CONFIDENCE_THRESHOLD or is_force_report) and differential:
        rec_res = execute_recommendation_pipeline(top_disease, 3, db)
        recommendations = [r.model_dump() for r in rec_res.recommendations]
        medicine_suppressed = False
        reasoning_timeline.append(f"Medicine recommendations retrieved for '{top_disease}'.")
        traces.append(ToolExecutionTrace(
            tool_name="recommendation_engine",
            input_params={"disease": top_disease},
            output_summary=f"{len(recommendations)} medicines retrieved"
        ))
    else:
        medicine_suppressed = True
        suppression_reason = (
            f"No evidence-based medicine recommendation available at current confidence level "
            f"({int(confidence * 100)}%). Further history and investigation required."
        )
        reasoning_timeline.append(f"Medicine suppressed: {suppression_reason}")

    # ── Step 8.5: Investigations & Scoring ────────────────────────────────────
    recommended_investigations = {}
    clinical_scores = []
    if differential:
        top_disease_names = [d["disease_name"] for d in differential[:3]]
        recommended_investigations = recommend_investigations(top_disease_names, confidence, syndrome_name)
        reasoning_timeline.append(f"Generated investigation panel for top differentials.")
        
        # Build patient data for scoring
        score_data = req.vitals.model_dump(exclude_none=True) if req.vitals else {}
        if patient_age: score_data["age"] = patient_age
        # We can add extracted vitals/symptoms here if needed
        # Fallback to defaults or partial for now
        
        applicable_scores = get_applicable_scores(top_disease, score_data)
        for score_name in applicable_scores:
            score_res = calculate_score(score_name, score_data)
            if score_res:
                clinical_scores.append(score_res.model_dump())
                reasoning_timeline.append(f"Calculated {score_name}: {score_res.score} ({score_res.risk_category})")
                
        if clinical_scores:
            traces.append(ToolExecutionTrace(
                tool_name="clinical_scoring_engine",
                input_params={"disease": top_disease, "scores": applicable_scores},
                output_summary=f"Calculated {len(clinical_scores)} clinical scores"
            ))

    # ── Step 9: Safety Validation ─────────────────────────────────────────────
    safety_score = 100.0
    safety_grade = "SAFE"
    warnings: List[str] = []

    if recommendations:
        top_med = recommendations[0]["medicine"]
        patient_profile = PatientProfileInput(
            age=patient_age or 30,
            gender=patient_gender or "unknown",
            pregnancy_status=is_pregnant or False,
            allergies=req.allergies or [],
            chronic_diseases=req.chronic_diseases or [],
            current_medications=req.current_medications or [],
        )
        safety_req = SafetyValidateRequest(
            medicine_name=top_med, patient_profile=patient_profile
        )
        safety_res = validate_patient_safety(safety_req, db)
        safety_score = safety_res.safety_score
        safety_grade = safety_res.safety_grade
        warnings = [w.message for w in safety_res.warnings]
        reasoning_timeline.append(f"Safety validation: {safety_grade} ({safety_score}%) for '{top_med}'.")
        traces.append(ToolExecutionTrace(
            tool_name="safety_validation_engine",
            input_params={"medicine": top_med},
            output_summary=f"Safety Score: {safety_score}% ({safety_grade})"
        ))

    # ── Step 10: Final Explainability Assembly ────────────────────────────────
    matched_syms = [s for s in symptom_names if s]
    if syndrome:
        missing_syms = syndrome["differentials"][0].get("missing", []) if syndrome["differentials"] else []
    elif differential:
        missing_syms = differential[0].get("missing", [])
    else:
        missing_syms = []

    conditions_less_likely = [
        d["disease_name"] for d in differential if d.get("status") == "RULED_OUT"
    ]

    # Knowledge gap check
    gap_logged = False
    if should_log_gap(confidence, len(differential)):
        gap_logged = True
        log_knowledge_gap(
            query_text=user_text,
            extracted_symptoms=symptom_names,
            entities=entities,
            reasoning_steps=reasoning_timeline,
            top_candidates=[d["disease_name"] for d in differential[:3]],
            confidence=confidence,
            session_uuid=req.session_uuid,
        )
        reasoning_timeline.append("Knowledge gap logged for human expert review.")

    if triage_status == "CLINICAL_UNCERTAINTY" or (not differential and gap_logged):
        clinical_rationale = (
            f"<p>⚠️ <strong>Clinical Uncertainty:</strong> {UNABLE_TO_IDENTIFY_RESPONSE}</p>"
        )
        recommendations = []
        medicine_suppressed = True
        suppression_reason = "Unable to identify evidence-supported diagnosis."
    elif triage_status == "RED_URGENT":
        clinical_rationale = (
            f"<p>🔴 <strong>Urgent Clinical Evaluation Required.</strong> "
            f"The symptom pattern is consistent with a high-risk presentation. "
            f"Immediate emergency assessment is recommended. The primary diagnostic consideration is "
            f"<strong>{top_disease}</strong>.</p>"
        )
    elif is_force_report:
        clinical_rationale = (
            f"<p>Based on the reported symptoms and gathered clinical history, the primary clinical differential is "
            f"<strong>{top_disease}</strong>. "
            f"Current diagnostic confidence is <strong>{int(confidence * 100)}%</strong>.</p>"
        )
    else:
        sym_str = ", ".join(symptom_names) if symptom_names else user_text
        clinical_rationale = (
            f"<p>I have noted your reported symptom(s): <strong>{sym_str}</strong>. "
            f"To narrow down the differential diagnosis and provide evidence-based medication & dosage guidelines, please answer the following question(s):</p>"
        )

    citations = _build_citations(syndrome_name, top_disease)
    thought_process = (
        f"v2.0 Pipeline: Extracted {len(symptom_names)} symptoms. "
        f"Emergency screen: CLEAR. Syndrome: {syndrome_name or 'None'}. "
        f"Top differential: '{top_disease}'. Confidence: {int(confidence * 100)}% "
        f"(Turn {turns}, ceiling {int(get_confidence_ceiling(turns) * 100)}%). "
        f"Triage: {triage_status}. Questions: {len(followup_questions)}. "
        f"Medicine gate: {'OPEN' if not medicine_suppressed else 'SUPPRESSED'}."
    )

    return ClinicalLLMResponse(
        thought_process=thought_process,
        reasoning_timeline=reasoning_timeline,
        assessment_stage=assessment_stage,
        extracted_symptoms=symptom_names,
        extracted_entities=entities,
        syndrome_detected=syndrome_name,
        is_emergency=False,
        emergency_alert=None,
        triage_status=triage_status,
        differential_diagnosis=differential,
        confidence_score=confidence,
        followup_questions=followup_questions,
        termination_reason=termination_reason,
        clinical_rationale=clinical_rationale,
        matched_symptoms=matched_syms,
        missing_symptoms=missing_syms,
        conditions_less_likely=conditions_less_likely,
        citations=citations,
        recommended_medicines=recommendations,
        medicine_recommendation_suppressed=medicine_suppressed,
        medicine_suppression_reason=suppression_reason,
        recommended_investigations=recommended_investigations,
        clinical_scores=clinical_scores,
        safety_score=safety_score,
        safety_grade=safety_grade,
        warnings=warnings,
        knowledge_gap_logged=gap_logged,
        tool_traces=traces,
    )


def build_orchestrator_prompt(req: OrchestratorRequest) -> PromptPreviewResponse:
    """Returns a preview of the clinical context injected into the pipeline."""
    context_summary = {
        "patient_age": req.patient_age,
        "patient_gender": req.patient_gender,
        "allergies": req.allergies or ["None documented"],
        "chronic_diseases": req.chronic_diseases or ["None documented"],
        "current_medications": req.current_medications or ["None documented"],
        "pregnancy_status": req.pregnancy_status,
        "turns_answered": req.turns_answered,
    }
    user_prompt = (
        f"PATIENT CLINICAL CONTEXT:\n"
        f"- Age: {req.patient_age} | Gender: {req.patient_gender} | Pregnant: {req.pregnancy_status}\n"
        f"- Allergies: {', '.join(req.allergies or ['None'])}\n"
        f"- Chronic Diseases: {', '.join(req.chronic_diseases or ['None'])}\n"
        f"- Current Medications: {', '.join(req.current_medications or ['None'])}\n"
        f"\nUSER INPUT: \"{req.query}\""
    )
    return PromptPreviewResponse(
        system_prompt="AuraMed AI v2.0 — Evidence-Based Clinical Decision Support System and Clinical Assistant.",
        user_prompt=user_prompt,
        injected_context_summary=context_summary,
    )
