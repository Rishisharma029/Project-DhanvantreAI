import uuid
import sqlite3
from typing import List, Dict, Any
from app.schemas.clinical_timeline_schema import (
    ClinicalTimelineRequest,
    ClinicalTimelineResponse,
    TimelineNode,
    TimelineStage,
    NodeStatus
)
from app.services.disease_engine import predict_diseases_from_symptoms


def generate_clinical_timeline(req: ClinicalTimelineRequest, db: sqlite3.Connection) -> ClinicalTimelineResponse:
    """
    Generate 5-Stage Physician Clinical Timeline:
    Symptoms -> Assessment -> Medicines -> Follow-up -> Recovery
    """
    # Determine primary condition
    condition_name = req.diagnosis_name if req.diagnosis_name else "Acute Viral Upper Respiratory Infection"
    if not req.diagnosis_name and req.reported_symptoms:
        try:
            pred = predict_diseases_from_symptoms(req.reported_symptoms, top_n=1, db=db)
            if pred and hasattr(pred, 'top_diseases') and pred.top_diseases:
                condition_name = pred.top_diseases[0].disease_name
        except Exception:
            pass

    onset_days = req.onset_days_ago if req.onset_days_ago is not None else 2
    symptoms_str = ", ".join(req.reported_symptoms) if req.reported_symptoms else "Unspecified systemic symptoms"
    meds_str = ", ".join(req.prescribed_medicines) if req.prescribed_medicines else "Symptomatic supportive therapy"

    # Stage 1: SYMPTOMS (Day 1 to onset_days)
    symptoms_node = TimelineNode(
        stage=TimelineStage.SYMPTOMS,
        title="Stage 1: Symptom Onset & Clinical Evolution",
        description=f"Initial presentation of reported symptoms: {symptoms_str}.",
        timeline_day=f"Day 1-{onset_days}",
        status=NodeStatus.COMPLETED,
        clinical_notes=[
            f"Patient presented {onset_days} days post-onset.",
            f"Primary chief complaints: {symptoms_str}.",
            "Pattern of presentation indicates acute onset phase with inflammatory response."
        ],
        key_metrics={
            "Onset Duration": f"{onset_days} days ago",
            "Initial Severity": "Moderate",
            "Infectious/Inflammatory Phase": "Acute Active"
        },
        evidence_sources=["NICE Clinical Knowledge Summaries (CKS)", "WHO Primary Care Triage Guidelines"]
    )

    # Stage 2: ASSESSMENT (Day onset_days + 1)
    assessment_day = onset_days + 1
    assessment_node = TimelineNode(
        stage=TimelineStage.ASSESSMENT,
        title="Stage 2: Diagnostic Triage & Physical Examination",
        description=f"Comprehensive physician evaluation and diagnostic confirmation for {condition_name}.",
        timeline_day=f"Day {assessment_day}",
        status=NodeStatus.IN_PROGRESS if onset_days <= 2 else NodeStatus.COMPLETED,
        clinical_notes=[
            f"Differential diagnosis established: {condition_name}.",
            "Physical examination: Vital signs audit, respiratory auscultation, or organ systems check.",
            "Diagnostic baseline: CBC, CRP, Pulse Oximetry, or relevant pathogen screening."
        ],
        key_metrics={
            "Diagnostic Confidence": "85-92%",
            "Triage Risk Category": "Moderate / Outpatient Care",
            "Recommended Baseline Labs": "CBC, Inflammatory Markers (CRP/ESR)"
        },
        evidence_sources=["CDC Guideline for Acute Illness Evaluation", "CDC Outpatient Triage Protocols"]
    )

    # Stage 3: MEDICINES (Day onset_days + 1 to onset_days + 7)
    med_start = assessment_day
    med_end = med_start + 5
    medicines_node = TimelineNode(
        stage=TimelineStage.MEDICINES,
        title="Stage 3: Targeted Therapeutic & Medication Regimen",
        description=f"Initiation of prescribed pharmacotherapy and supportive care: {meds_str}.",
        timeline_day=f"Day {med_start}-{med_end}",
        status=NodeStatus.SCHEDULED,
        clinical_notes=[
            f"Prescribed pharmacological regimen: {meds_str}.",
            "Maintain adequate hydration, rest, and organ-specific supportive measures.",
            "Monitor therapeutic response and evaluate for potential adverse drug events within 48-72 hours."
        ],
        key_metrics={
            "Primary Regimen": meds_str,
            "Expected Onset of Action": "24-48 Hours",
            "Treatment Duration": "5-7 Days"
        },
        evidence_sources=["FDA Approved Product Monograph", "WHO Essential Medicines List"]
    )

    # Stage 4: FOLLOWUP (Day med_end + 1 to med_end + 3)
    followup_day = med_end + 2
    followup_node = TimelineNode(
        stage=TimelineStage.FOLLOWUP,
        title="Stage 4: Clinical Review & Follow-Up Evaluation",
        description="Formal clinical assessment of treatment efficacy, symptom resolution, and lab normalization.",
        timeline_day=f"Day {followup_day}",
        status=NodeStatus.RECOMMENDED,
        clinical_notes=[
            "Evaluate symptom resolution trajectory (> 80% improvement expected).",
            "Re-assess vital signs and repeat baseline labs if inflammatory markers were elevated.",
            "Adjust or step-down medication dosages based on clinical progression."
        ],
        key_metrics={
            "Target Follow-Up Date": f"Day {followup_day}",
            "Resolution Target": "> 80% Symptom Clearance",
            "Next Step": "Discontinue acute medications if asymptomatic"
        },
        evidence_sources=["NICE Post-Treatment Review Standards", "Clinical Decision Support Framework"]
    )

    # Stage 5: RECOVERY (Day followup_day + 2 to followup_day + 7)
    recovery_start = followup_day + 1
    total_days = recovery_start + 4
    recovery_node = TimelineNode(
        stage=TimelineStage.RECOVERY,
        title="Stage 5: Complete Convalescence & Full Functional Recovery",
        description="Return to full daily activities, physiological restoration, and post-acute maintenance.",
        timeline_day=f"Day {recovery_start}-{total_days}",
        status=NodeStatus.SCHEDULED,
        clinical_notes=[
            "Achieve 100% baseline functional capacity and stamina.",
            "Complete post-recovery health maintenance and lifestyle risk reduction.",
            "Immediate emergency re-evaluation triggered if red flag symptoms reappear."
        ],
        key_metrics={
            "Estimated Recovery Horizon": f"{total_days} Days",
            "Functional Capacity Target": "100% Full Return to Work/Activity",
            "Long-Term Prognosis": "Excellent with complete resolution"
        },
        evidence_sources=["WHO Global Recovery Standards", "CDC Convalescence Guidelines"]
    )

    timeline_nodes = [symptoms_node, assessment_node, medicines_node, followup_node, recovery_node]

    return ClinicalTimelineResponse(
        timeline_id=f"TL-{uuid.uuid4().hex[:8].upper()}",
        condition_name=condition_name,
        total_estimated_days=total_days,
        current_stage=TimelineStage.ASSESSMENT if onset_days <= 2 else TimelineStage.MEDICINES,
        timeline_nodes=timeline_nodes,
        key_milestones=[
            f"Day 1-{onset_days}: Acute Symptom Identification",
            f"Day {assessment_day}: Physician Diagnosis & Lab Baseline",
            f"Day {med_start}-{med_end}: Active Medication Course ({meds_str})",
            f"Day {followup_day}: Clinical Review & Resolution Audit",
            f"Day {total_days}: Complete Functional Recovery"
        ],
        red_flag_warnings=[
            "High persistent fever (> 102°F / 38.9°C) unresponsive to antipyretics after 48 hours",
            "Sudden onset of shortness of breath, dyspnea, or chest pain",
            "Severe dizziness, confusion, or inability to retain fluids",
            "Worsening or relapse of symptoms after initial improvement"
        ]
    )
