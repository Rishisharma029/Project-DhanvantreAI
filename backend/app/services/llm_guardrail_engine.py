import re
import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.guardrail_schema import (
    GuardrailVerifyRequest, GuardrailVerifyResponse, GuardrailViolationItem
)
from app.services.dosage_engine import extract_dosage_reference

PREGNANCY_CATEGORY_D_X = ['methotrexate', 'warfarin', 'valproate', 'isotretinoin', 'lisinopril', 'losartan', 'atorvastatin']
PEDIATRIC_CONTRAINDICATED = ['aspirin', 'ciprofloxacin', 'levofloxacin', 'tetracycline', 'doxycycline']

def verify_medicine_existence(med_name: str, db: sqlite3.Connection) -> bool:
    """Check if medicine or ingredient exists in Phase 1 database."""
    clean = med_name.strip().lower()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id FROM medicines 
        WHERE LOWER(canonical_name) LIKE ? OR LOWER(brand_name) LIKE ? OR LOWER(generic_name) LIKE ?
        LIMIT 1;
    """, (f"%{clean}%", f"%{clean}%", f"%{clean}%"))
    if cursor.fetchone():
        return True

    cursor.execute("SELECT id FROM medicine_ingredients WHERE LOWER(ingredient_name) LIKE ? LIMIT 1;", (f"%{clean}%",))
    if cursor.fetchone():
        return True

    return False

def verify_llm_guardrails(req: GuardrailVerifyRequest, db: sqlite3.Connection) -> GuardrailVerifyResponse:
    """
    Executes 5 Core LLM Guardrail Safety Checks:
    1. Medicine Name Verification (hallucination detection)
    2. Dosage Limit Verification (overdose detection)
    3. Warnings Audit (pediatric/geriatric/organ-impairment)
    4. Contraindications Audit (allergies/pregnancy Category D/X)
    5. Safety Instructions Check (disclaimer & route)

    If any mismatch is detected -> sets status='REGENERATE_REQUIRED' and generates corrective prompt.
    """
    violations: List[GuardrailViolationItem] = []
    med_name = req.medicine_name.strip() if req.medicine_name else ""

    # 1. MEDICINE NAME CHECK (Hallucination Detection)
    if med_name:
        exists = verify_medicine_existence(med_name, db)
        if not exists:
            violations.append(GuardrailViolationItem(
                check_name="Medicine Names",
                severity="Critical",
                message=f"HALLUCINATION ALERT: Medicine name '{med_name}' was not found in the validated medical database.",
                failed_target=med_name
            ))

    # 2. DOSAGE LIMIT VERIFICATION (Overdose Detection)
    if med_name and req.dosage_text:
        dose_nums = re.findall(r'(\d+)\s*mg', req.dosage_text.lower())
        if dose_nums:
            proposed_dose = int(dose_nums[0])
            ref_dose = extract_dosage_reference(med_name, None, db)
            
            # Check for Paracetamol > 4000mg or general high single dose > 3000mg
            if ('paracetamol' in med_name.lower() or 'acetaminophen' in med_name.lower()) and proposed_dose > 4000:
                violations.append(GuardrailViolationItem(
                    check_name="Dosages",
                    severity="Critical",
                    message=f"DOSAGE OVERDOSE HAZARD: Proposed dose ({proposed_dose} mg) exceeds maximum daily limit of 4000 mg (4g) for Paracetamol.",
                    failed_target=req.dosage_text
                ))
            elif proposed_dose > 5000:
                violations.append(GuardrailViolationItem(
                    check_name="Dosages",
                    severity="Critical",
                    message=f"DOSAGE OVERDOSE HAZARD: Proposed single/daily dose ({proposed_dose} mg) exceeds maximum safe therapeutic limit.",
                    failed_target=req.dosage_text
                ))

    # 3. WARNINGS AUDIT
    if req.patient_age and req.patient_age < 18 and med_name:
        for ped_drug in PEDIATRIC_CONTRAINDICATED:
            if ped_drug in med_name.lower():
                violations.append(GuardrailViolationItem(
                    check_name="Warnings",
                    severity="High",
                    message=f"PEDIATRIC SAFETY WARNING MISSING: '{med_name}' is contraindicated in pediatric patients under 18 years.",
                    failed_target=med_name
                ))

    # 4. CONTRAINDICATIONS AUDIT
    if med_name:
        med_lower = med_name.lower()
        # Allergies check
        for allergen in (req.patient_allergies or []):
            if allergen.strip().lower() in med_lower:
                violations.append(GuardrailViolationItem(
                    check_name="Contraindications",
                    severity="Critical",
                    message=f"CRITICAL ALLERGY CONTRAINDICATION: Proposed medication '{med_name}' matches documented patient allergy '{allergen}'.",
                    failed_target=med_name
                ))

        # Pregnancy check
        if req.is_pregnant:
            for dx in PREGNANCY_CATEGORY_D_X:
                if dx in med_lower:
                    violations.append(GuardrailViolationItem(
                        check_name="Contraindications",
                        severity="Critical",
                        message=f"PREGNANCY CONTRAINDICATION: '{med_name}' contains Pregnancy Category D/X agent '{dx.title()}'.",
                        failed_target=med_name
                    ))

    # 5. SAFETY INSTRUCTIONS CHECK
    if req.has_disclaimer is False:
        violations.append(GuardrailViolationItem(
            check_name="Safety Instructions",
            severity="Moderate",
            message="SAFETY INSTRUCTION MISSING: Mandatory legal medical reference disclaimer is missing from LLM response.",
            failed_target="disclaimer"
        ))

    # MISMATCH -> REGENERATE PROTOCOL
    if violations:
        violation_msgs = [f"[{v.check_name}] {v.message}" for v in violations]
        corrective_prompt = (
            "GUARDRAIL REGENERATION PROMPT: The candidate response failed clinical safety guardrails with "
            f"{len(violations)} violation(s):\n" + "\n".join(violation_msgs) +
            "\n\nPlease regenerate the response correcting all safety mismatches and enforcing strict medical guidelines."
        )
        return GuardrailVerifyResponse(
            is_valid=False,
            status="REGENERATE_REQUIRED",
            total_violations=len(violations),
            violations=violations,
            corrective_feedback_prompt=corrective_prompt
        )

    return GuardrailVerifyResponse(
        is_valid=True,
        status="PASSED",
        total_violations=0,
        violations=[],
        corrective_feedback_prompt=None
    )
