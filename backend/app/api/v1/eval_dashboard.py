"""
AuraMed AI — Evaluation Dashboard API
=========================================
Serves live clinical validation metrics at GET /api/v1/eval/metrics
Reads from failure reports in clinical_validation/failures/
"""
import json
import os
import glob
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import APIRouter

router = APIRouter(prefix="/eval", tags=["Evaluation Dashboard"])

FAILURE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..",
    "clinical_validation", "failures"
)


def _load_latest_report() -> Optional[Dict[str, Any]]:
    """Loads the most recent validation failure report."""
    os.makedirs(FAILURE_DIR, exist_ok=True)
    reports = sorted(glob.glob(os.path.join(FAILURE_DIR, "failure_report_*.json")), reverse=True)
    if not reports:
        return None
    try:
        with open(reports[0], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _get_disease_kb_count() -> int:
    try:
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        from app.data.disease_kb import DISEASE_COUNT
        return DISEASE_COUNT
    except Exception:
        return 0


def _get_question_bank_count() -> int:
    try:
        from app.services.clinical_question_bank import HIERARCHICAL_QUESTION_BANK
        return len(HIERARCHICAL_QUESTION_BANK)
    except Exception:
        return 0


def _count_validation_cases() -> Dict[str, int]:
    val_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "..",
        "clinical_validation"
    )
    counts = {"total": 0}
    if not os.path.exists(val_dir):
        return counts
    for spec_dir in os.listdir(val_dir):
        full = os.path.join(val_dir, spec_dir)
        if os.path.isdir(full) and spec_dir != "failures":
            n = len(glob.glob(os.path.join(full, "*.json")))
            if n > 0:
                counts[spec_dir] = n
                counts["total"] += n
    return counts


@router.get("/metrics")
def get_eval_metrics() -> Dict[str, Any]:
    """Returns current evaluation metrics for the dashboard."""
    report = _load_latest_report()
    case_counts = _count_validation_cases()

    if report:
        summary = report.get("summary", {})
        failures = report.get("failures", [])
        top_failure_specialties = sorted(
            summary.get("failures_by_specialty", {}).items(),
            key=lambda x: x[1], reverse=True
        )[:5]
    else:
        summary = {}
        failures = []
        top_failure_specialties = []

    return {
        "last_run": summary.get("timestamp", "Never"),
        "knowledge_base": {
            "diseases": _get_disease_kb_count(),
            "questions": _get_question_bank_count(),
            "validation_cases": case_counts.get("total", 0),
            "cases_by_specialty": {k: v for k, v in case_counts.items() if k != "total"},
        },
        "accuracy_metrics": {
            "triage_accuracy_pct": summary.get("triage_accuracy_pct", 0),
            "top1_accuracy_pct": summary.get("top1_accuracy_pct", 0),
            "top3_accuracy_pct": summary.get("top3_accuracy_pct", 0),
            "emergency_detection_pct": summary.get("emergency_detection_pct", 0),
            "pass_rate_pct": summary.get("pass_rate_pct", 0),
        },
        "safety_metrics": {
            "hallucination_rate_pct": summary.get("hallucination_rate_pct", 0),
            "hallucinations_total": summary.get("hallucinations", 0),
            "false_emergency_count": summary.get("false_emergency", 0),
            "missed_emergency_count": summary.get("missed_emergency", 0),
            "medicine_gate_violations": summary.get("medicine_gate_violations", 0),
        },
        "case_metrics": {
            "total_cases_tested": summary.get("total_cases", 0),
            "all_pass": summary.get("all_pass", 0),
            "failure_count": summary.get("failure_count", 0),
        },
        "top_failure_specialties": top_failure_specialties,
        "recent_failures": [
            {
                "case_id": f.get("case_id"),
                "specialty": f.get("specialty"),
                "diagnosis": f.get("final_diagnosis"),
                "failures": f.get("failures", [])[:2],
            }
            for f in failures[:10]
        ],
    }


@router.get("/run")
def trigger_validation_run() -> Dict[str, Any]:
    """Triggers a fresh validation run. Returns immediately with run ID."""
    from datetime import datetime, timezone
    run_id = datetime.now(timezone.utc).strftime("RUN_%Y%m%dT%H%M%SZ")
    return {
        "run_id": run_id,
        "status": "QUEUED",
        "message": "Run the validation manually: python clinical_validation/run_validation.py",
        "note": "Background validation runs not yet implemented. Use CLI runner.",
    }
