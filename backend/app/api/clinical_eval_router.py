import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.services.clinical_metrics_service import evaluate_gold_suite_metrics
from app.services.clinical_audit_ledger import get_all_clinical_failures

router = APIRouter(prefix="/clinical-eval", tags=["Clinical Validation & Evaluation Suite ⭐⭐⭐⭐⭐"])

@router.get("/accuracy-report")
def get_accuracy_report():
    """
    Returns quantitative clinical metrics evaluating the Gold Test Suite:
    - Emergency Detection Accuracy (%)
    - Drug Interaction & Safety Accuracy (%)
    - Differential Top-3 Accuracy (%)
    - Hallucination & Repeated Question Rates (%)
    """
    return evaluate_gold_suite_metrics()

@router.get("/failure-log")
def get_clinical_failure_log(db: sqlite3.Connection = Depends(get_db)):
    """
    Returns the persistent AI Failure Log ledger tracking categorized clinical errors and resolutions.
    """
    return get_all_clinical_failures(db)
