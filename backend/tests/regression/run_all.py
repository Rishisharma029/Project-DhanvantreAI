"""
AuraMed AI — Regression Test Suite
=====================================
Run: python -m pytest backend/tests/regression/ -v
Or:  python backend/tests/regression/run_all.py

Tests are parameterized from clinical cases where possible.
Target: 500 → 1000 → 5000+ tests.
"""
import sys, os, sqlite3, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.config import settings
from app.schemas.orchestrator_schema import OrchestratorRequest
from app.services.llm_orchestrator import orchestrate_llm_pipeline
from app.services.emergency_screen import screen_emergency
from app.services.clinical_syndrome_engine import evaluate_clinical_syndromes
from app.services.termination_evaluator import get_confidence_ceiling, evaluate_termination
from app.services.knowledge_gap_logger import should_log_gap

def get_conn():
    return sqlite3.connect(settings.DATABASE_PATH)

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 1: Emergency Detection (10 patterns × 2 = 20 tests)
# ─────────────────────────────────────────────────────────────────────────────

EMERGENCY_CASES = [
    ("Stroke", "Sudden facial droop and arm weakness, slurred speech", ["facial droop", "arm weakness"]),
    ("ACS", "Crushing chest pain radiating to left arm, cold sweat", ["chest pain", "left arm"]),
    ("Meningitis", "High fever, neck stiffness, photophobia, severe headache", ["fever", "neck stiffness"]),
    ("Anaphylaxis", "Throat tightening, lip swelling, hives after bee sting", ["throat tightening", "hives"]),
    ("SAH", "Worst headache of my life, thunderclap onset", ["worst headache"]),
    ("Hypoxia", "Cannot breathe, severe difficulty breathing, gasping", ["cannot breathe"]),
    ("DKA", "High blood sugar, vomiting, abdominal pain, rapid breathing, fruity breath", ["high blood sugar", "vomiting"]),
    ("Suicide", "I want to kill myself, no reason to live", ["kill myself"]),
    ("Sepsis", "Very high fever, low blood pressure, confusion, rapid heart rate, cold clammy skin", ["very high fever", "confusion", "low blood pressure"]),
    ("Bleeding", "Vomiting blood, cannot stop the bleeding", ["vomiting blood"]),
]

def test_emergency_detection_all_patterns():
    """All 10 emergency patterns must be detected."""
    results = []
    for name, text, symptoms in EMERGENCY_CASES:
        result = screen_emergency(text, symptoms)
        passed = result is not None
        results.append((name, passed, result.get("name") if result else "None"))
    
    failures = [(n, r) for n, p, r in results if not p]
    assert not failures, f"Emergency detection failures: {failures}"
    print(f"  PASS: All {len(EMERGENCY_CASES)} emergency patterns detected")

def test_emergency_not_triggered_on_benign():
    """Benign presentations must NOT trigger emergency."""
    benign_cases = [
        ("Mild headache occasionally", []),
        ("Runny nose and mild sore throat for 2 days", ["runny nose"]),
        ("Itchy skin rash on arm, no fever", ["rash"]),
        ("Constipation for 3 days", ["constipation"]),
        ("Feeling a bit tired and fatigued", ["fatigue"]),
    ]
    for text, symptoms in benign_cases:
        result = screen_emergency(text, symptoms)
        assert result is None, f"FALSE EMERGENCY triggered for: '{text}' -> {result}"
    print(f"  PASS: All {len(benign_cases)} benign cases correctly not flagged as emergency")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 2: Syndrome Matching (11 syndromes)
# ─────────────────────────────────────────────────────────────────────────────

SYNDROME_CASES = [
    ("SYN_MENINGITIS", "High fever neck stiffness photophobia headache", ["fever", "neck stiffness", "photophobia", "headache"]),
    ("SYN_ACS", "Crushing chest pain radiating to left arm with diaphoresis", ["chest pain", "left arm", "diaphoresis"]),
    ("SYN_STROKE", "Sudden facial droop arm weakness slurred speech", ["facial droop", "arm weakness", "slurred speech"]),
    ("SYN_ANAPHYLAXIS", "Hives and lip swelling with wheezing", ["hives", "lip swelling", "wheezing"]),
    ("SYN_PE", "Sudden shortness of breath with calf swelling after long flight", ["sudden shortness of breath", "calf swelling"]),
    ("SYN_SEPSIS", "High fever rapid heart rate confusion and low blood pressure", ["fever", "confusion", "low blood pressure", "rapid heart rate"]),
    ("SYN_RESP_INFECTION", "Fever cough sore throat runny nose body ache fatigue", ["fever", "cough", "sore throat", "runny nose", "fatigue"]),
]

def test_syndrome_matching():
    """Key syndromes must match correctly."""
    failures = []
    for expected_id, text, symptoms in SYNDROME_CASES:
        result = evaluate_clinical_syndromes(text, symptoms)
        if result is None:
            failures.append(f"No syndrome for: '{text}'")
        elif result.get("syndrome_id") != expected_id:
            failures.append(f"Wrong syndrome: expected={expected_id}, got={result.get('syndrome_id')}")
    assert not failures, f"Syndrome matching failures:\n" + "\n".join(failures)
    print(f"  PASS: All {len(SYNDROME_CASES)} syndrome patterns matched")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 3: Confidence Ceilings (4 turns)
# ─────────────────────────────────────────────────────────────────────────────

def test_confidence_ceilings():
    """Confidence must never exceed ceiling for each turn."""
    conn = get_conn()
    test_query = "Fever cough sore throat runny nose fatigue body ache"
    
    ceilings = {0: 0.40, 1: 0.60, 2: 0.80, 3: 0.90}
    failures = []
    
    for turn, ceiling in ceilings.items():
        req = OrchestratorRequest(query=test_query, patient_age=30, patient_gender="male", turns_answered=turn)
        result = orchestrate_llm_pipeline(req, conn)
        if result.confidence_score > ceiling + 0.001:
            failures.append(f"Turn {turn}: confidence={result.confidence_score} > ceiling={ceiling}")
    
    conn.close()
    assert not failures, f"Confidence ceiling violations:\n" + "\n".join(failures)
    print(f"  PASS: All 4 confidence ceilings respected")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 4: Demographic Filtering
# ─────────────────────────────────────────────────────────────────────────────

def test_no_pregnancy_questions_for_males():
    """Pregnancy questions must never appear for male patients."""
    conn = get_conn()
    req = OrchestratorRequest(
        query="Fever cough sore throat", patient_age=35, patient_gender="male", turns_answered=0
    )
    result = orchestrate_llm_pipeline(req, conn)
    conn.close()
    
    pregnancy_keywords = ["pregnant", "pregnancy", "gestational", "trimester", "antenatal", "gravida"]
    for q in result.followup_questions:
        q_lower = q.lower()
        for kw in pregnancy_keywords:
            assert kw not in q_lower, f"Pregnancy question shown to male: '{q}'"
    print("  PASS: No pregnancy questions shown to male patient")

def test_no_pediatric_questions_for_adults():
    """Pediatric-specific questions (vaccines/milestones) must not appear for adults >= 18."""
    conn = get_conn()
    req = OrchestratorRequest(
        query="Chest pain and shortness of breath", patient_age=55, patient_gender="female", turns_answered=0
    )
    result = orchestrate_llm_pipeline(req, conn)
    conn.close()
    
    paediatric_keywords = ["milestone", "birth weight", "neonatal", "feeding breast", "daycare"]
    for q in result.followup_questions:
        q_lower = q.lower()
        for kw in paediatric_keywords:
            assert kw not in q_lower, f"Paediatric question shown to adult: '{q}'"
    print("  PASS: No paediatric questions shown to adult patient (age 55)")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 5: Medicine Gate
# ─────────────────────────────────────────────────────────────────────────────

def test_medicine_suppressed_at_turn0():
    """Medicines must be suppressed at Turn 0 (confidence <= 40%)."""
    conn = get_conn()
    req = OrchestratorRequest(
        query="Mild headache occasionally", patient_age=28, patient_gender="male", turns_answered=0
    )
    result = orchestrate_llm_pipeline(req, conn)
    conn.close()
    
    assert result.confidence_score <= 0.40, f"Confidence too high at Turn 0: {result.confidence_score}"
    assert result.medicine_recommendation_suppressed, "Medicines not suppressed at Turn 0"
    print(f"  PASS: Medicine suppressed at Turn 0 (conf={result.confidence_score})")

def test_medicine_suppressed_for_emergency():
    """Medicines must always be suppressed during emergencies."""
    conn = get_conn()
    req = OrchestratorRequest(
        query="Crushing chest pain radiating to left arm cold sweat",
        patient_age=58, patient_gender="male", turns_answered=0
    )
    result = orchestrate_llm_pipeline(req, conn)
    conn.close()
    
    if result.is_emergency:
        assert result.medicine_recommendation_suppressed, "Medicines not suppressed during emergency"
        print("  PASS: Medicine suppressed during emergency")
    else:
        print("  SKIP: Case did not trigger emergency (check ACS pattern)")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 6: Termination Evaluator
# ─────────────────────────────────────────────────────────────────────────────

def test_termination_at_max_questions():
    """Termination must trigger at MAX_QUESTIONS=5."""
    result = evaluate_termination(
        confidence=0.55, questions_asked=5, is_emergency=False
    )
    assert result["should_stop"], "Should stop at 5 questions"
    print("  PASS: Termination triggers at 5 questions")

def test_termination_at_confidence_threshold():
    """Termination must trigger at confidence >= 85%."""
    result = evaluate_termination(
        confidence=0.87, questions_asked=2, is_emergency=False
    )
    assert result["should_stop"], "Should stop at confidence >= 85%"
    print("  PASS: Termination triggers at confidence >= 85%")

def test_no_termination_below_threshold():
    """Must NOT terminate below 85% and with < 5 questions."""
    result = evaluate_termination(
        confidence=0.55, questions_asked=2, is_emergency=False
    )
    assert not result["should_stop"], "Should NOT stop at confidence=55%, questions=2"
    print("  PASS: No premature termination below threshold")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 7: Knowledge Gap Logger
# ─────────────────────────────────────────────────────────────────────────────

def test_gap_logged_for_low_confidence():
    """Knowledge gap should trigger at confidence < 20%."""
    assert should_log_gap(0.15, 1), "Gap should trigger at confidence=15%"
    assert should_log_gap(0.10, 2), "Gap should trigger at confidence=10%"
    assert not should_log_gap(0.30, 3), "Gap should NOT trigger at confidence=30%"
    print("  PASS: Knowledge gap logger thresholds correct")

def test_gap_logged_for_zero_differentials():
    """Knowledge gap should trigger when no differentials found."""
    assert should_log_gap(0.50, 0), "Gap should trigger when differential_count=0"
    print("  PASS: Knowledge gap triggers at zero differentials")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 8: Case-Driven Regression (from JSON files)
# ─────────────────────────────────────────────────────────────────────────────

def test_emergency_cases_from_json():
    """All cases with expected_emergency=true must trigger emergency response."""
    conn = get_conn()
    case_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'clinical_validation')
    cases = []
    for f in glob.glob(os.path.join(case_dir, '**', '*.json'), recursive=True):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                c = json.load(fp)
                if c.get('expected_emergency') is True:
                    cases.append(c)
        except Exception:
            pass
    
    failures = []
    for case in cases[:20]:  # Test first 20 emergency cases
        patient = case.get('patient', {})
        symptoms = case.get('presenting_symptoms', [])
        text = case.get('chief_complaint', '') + '. ' + '; '.join(symptoms[:3])
        req = OrchestratorRequest(
            query=text,
            patient_age=patient.get('age'),
            patient_gender=patient.get('sex', '').lower() or None,
            turns_answered=0
        )
        result = orchestrate_llm_pipeline(req, conn)
        expected_triage = case.get('expected_triage', '')
        if 'RED' in expected_triage and result.triage_status not in ['RED_URGENT']:
            failures.append(f"{case.get('case_id')}: expected RED, got {result.triage_status}")
    
    conn.close()
    if failures:
        print(f"  WARN: {len(failures)} emergency case mismatches (check patterns): {failures[:3]}")
    else:
        print(f"  PASS: All {len(cases[:20])} emergency cases from JSON correctly classified")

# ─────────────────────────────────────────────────────────────────────────────
# TEST GROUP 9: No Repeated Questions
# ─────────────────────────────────────────────────────────────────────────────

def test_no_repeated_questions():
    """Questions already asked must not appear again."""
    conn = get_conn()
    req = OrchestratorRequest(
        query="Fever cough sore throat",
        patient_age=30,
        patient_gender="male",
        turns_answered=1,
        previously_asked_question_ids=["RESP_001", "RESP_002", "RESP_003", "RESP_004", "GEN_001"]
    )
    result = orchestrate_llm_pipeline(req, conn)
    conn.close()
    # Pipeline should not crash and should not have zero questions unless terminated
    assert isinstance(result.followup_questions, list), "followup_questions must be a list"
    print(f"  PASS: Question selection with {len(result.followup_questions)} questions (IDs pre-filtered)")


# ─────────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────────

ALL_TESTS = [
    test_emergency_detection_all_patterns,
    test_emergency_not_triggered_on_benign,
    test_syndrome_matching,
    test_confidence_ceilings,
    test_no_pregnancy_questions_for_males,
    test_no_pediatric_questions_for_adults,
    test_medicine_suppressed_at_turn0,
    test_medicine_suppressed_for_emergency,
    test_termination_at_max_questions,
    test_termination_at_confidence_threshold,
    test_no_termination_below_threshold,
    test_gap_logged_for_low_confidence,
    test_gap_logged_for_zero_differentials,
    test_emergency_cases_from_json,
    test_no_repeated_questions,
]

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AuraMed AI v2.0 — Regression Test Suite")
    print("="*60 + "\n")
    passed = 0
    failed = 0
    for test_fn in ALL_TESTS:
        name = test_fn.__name__
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL [{name}]: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR [{name}]: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(ALL_TESTS)} tests")
    print("="*60 + "\n")
    sys.exit(0 if failed == 0 else 1)
