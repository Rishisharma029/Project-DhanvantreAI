"""
AuraMed AI — Termination Evaluator
=====================================
Determines when adaptive questioning should STOP.
Prevents over-questioning while ensuring sufficient clinical information.

Stop criteria (any one triggers termination):
  1. Confidence >= 85%
  2. Total questions asked >= 5
  3. Emergency detected
  4. Investigation clearly required (high suspicion of serious disease)
  5. No new information gain possible (all key questions answered)
"""
from typing import Dict, Any, List, Optional


INVESTIGATION_TRIGGER_DISEASES = {
    "Bacterial Meningitis",
    "Acute Myocardial Infarction",
    "Pulmonary Embolism",
    "Subarachnoid Hemorrhage",
    "Acute Appendicitis",
    "Aortic Dissection",
    "Septic Shock",
    "Diabetic Ketoacidosis",
    "Stroke",
    "Acute Coronary Syndrome",
}

MAX_QUESTIONS = 5
CONFIDENCE_THRESHOLD = 0.85


def evaluate_termination(
    confidence: float,
    questions_asked: int,
    is_emergency: bool,
    top_differential: Optional[str] = None,
    previously_asked_ids: Optional[List[str]] = None,
    total_bank_available: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Evaluates whether adaptive questioning should stop.

    Returns:
        {
            "should_stop": bool,
            "reason": str   — human-readable termination reason
        }
    """
    # Rule 1: Emergency detected
    if is_emergency:
        return {
            "should_stop": True,
            "reason": "Emergency detected — immediate evaluation required. No further questions."
        }

    # Rule 2: Confidence threshold reached
    if confidence >= CONFIDENCE_THRESHOLD:
        return {
            "should_stop": True,
            "reason": f"Confidence has reached {int(confidence * 100)}% — sufficient clinical evidence gathered."
        }

    # Rule 3: Max questions reached
    if questions_asked >= MAX_QUESTIONS:
        return {
            "should_stop": True,
            "reason": f"Maximum of {MAX_QUESTIONS} follow-up questions reached — recommending clinical investigation."
        }

    # Rule 4: High-suspicion disease requiring investigation
    if top_differential and top_differential in INVESTIGATION_TRIGGER_DISEASES:
        if confidence >= 0.60:
            return {
                "should_stop": True,
                "reason": f"High suspicion for '{top_differential}' — clinical investigation (laboratory/imaging) recommended before further questioning."
            }

    # Rule 5: All available questions exhausted
    if (previously_asked_ids is not None and total_bank_available is not None
            and len(previously_asked_ids) >= total_bank_available):
        return {
            "should_stop": True,
            "reason": "All available diagnostic questions have been answered."
        }

    return {"should_stop": False, "reason": ""}


def get_assessment_stage(turns: int) -> str:
    """Returns the clinical assessment stage label based on conversation turn count."""
    stages = {
        0: "Adaptive Questioning (Turn 1)",
        1: "Clarifying Follow-up (Turn 2)",
        2: "Clinical History Gathered (Turn 3)",
        3: "Full Clinical Evaluation",
    }
    return stages.get(min(turns, 3), "Full Clinical Evaluation")


def get_confidence_ceiling(turns: int) -> float:
    """Returns the maximum allowable confidence score for the given turn."""
    ceilings = {0: 0.40, 1: 0.60, 2: 0.80, 3: 0.90}
    return ceilings.get(min(turns, 3), 0.92)
