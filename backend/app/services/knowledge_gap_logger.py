"""
AuraMed AI — Knowledge Gap Logger
===================================
When the clinical reasoning engine cannot match any syndrome or disease with
sufficient confidence, it logs the case for human expert review.

Key rules:
  - NEVER hallucinate a diagnosis to fill a gap.
  - NEVER invent a medicine or guideline.
  - Log the gap and return a safe "Unable to identify" response.
  - All gaps are reviewed by human experts before any learning occurs.
"""
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


GAP_LOG_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "knowledge_gaps"
)


def log_knowledge_gap(
    query_text: str,
    extracted_symptoms: List[str],
    entities: Dict[str, Any],
    reasoning_steps: List[str],
    top_candidates: List[str],
    confidence: float,
    session_uuid: Optional[str] = None,
) -> str:
    """
    Logs an unresolved clinical case to the knowledge gap repository.
    Returns the path of the saved log file.
    """
    os.makedirs(GAP_LOG_DIR, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"gap_{timestamp}.json"
    filepath = os.path.join(GAP_LOG_DIR, filename)

    gap_record = {
        "gap_id": f"GAP_{timestamp}",
        "session_uuid": session_uuid or "unknown",
        "timestamp": timestamp,
        "status": "PENDING_REVIEW",
        "query": query_text,
        "extracted_symptoms": extracted_symptoms,
        "extracted_entities": entities,
        "reasoning_steps": reasoning_steps,
        "top_candidate_diseases": top_candidates,
        "final_confidence": confidence,
        "resolution": None,
        "reviewed_by": None,
        "note": (
            "This case could not be matched to an evidence-supported diagnosis. "
            "Human expert review is required before any learning update."
        ),
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(gap_record, f, indent=2, ensure_ascii=False)

    return filepath


UNABLE_TO_IDENTIFY_RESPONSE = (
    "I was unable to identify an evidence-supported diagnosis based on the information provided. "
    "This does not mean nothing is wrong — it means the information collected does not clearly "
    "match a recognizable clinical pattern in my knowledge base. "
    "Please consult a licensed physician for a proper evaluation."
)


def should_log_gap(confidence: float, differential_count: int) -> bool:
    """Returns True if the case should be logged as a knowledge gap."""
    return confidence < 0.20 or differential_count == 0
