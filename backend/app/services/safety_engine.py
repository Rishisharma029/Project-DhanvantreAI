import sqlite3
from typing import List, Dict, Any, Optional
from app.schemas.safety_schema import (
    PatientProfileInput, SafetyValidateRequest, SafetyValidateResponse, SafetyWarningItem
)
from app.services.interaction_engine import check_pairwise_interaction

# High-risk drug classifications for organ toxicity & age
NEPHROTOXIC_DRUGS = ['ibuprofen', 'naproxen', 'aspirin', 'diclofenac', 'gentamicin', 'amikacin', 'vancomycin', 'cisplatin']
HEPATOTOXIC_DRUGS = ['ketoconazole', 'methotrexate', 'paracetamol', 'acetaminophen', 'isoniazid', 'rifampicin']
PEDIATRIC_CONTRAINDICATED = ['aspirin', 'ciprofloxacin', 'levofloxacin', 'tetracycline', 'doxycycline']
GERIATRIC_HIGH_RISK = ['diazepam', 'alprazolam', 'chlordiazepoxide', 'diphenhydramine', 'chlorpheniramine']

PREGNANCY_CATEGORY_D_X = ['methotrexate', 'warfarin', 'valproate', 'isotretinoin', 'lisinopril', 'losartan', 'atorvastatin']

def resolve_medicine_ingredients_list(med_name: str, db: sqlite3.Connection) -> List[str]:
    """Retrieve all active ingredients for a medicine or fallback to query name."""
    clean_name = med_name.strip().lower()
    cursor = db.cursor()
    cursor.execute("""
        SELECT DISTINCT ingredient_name 
        FROM medicine_ingredients mi
        JOIN medicines m ON mi.medicine_id = m.id
        WHERE LOWER(m.canonical_name) LIKE ? OR LOWER(m.brand_name) LIKE ?;
    """, (f"%{clean_name}%", f"%{clean_name}%"))
    rows = cursor.fetchall()
    if rows:
        return [r[0].lower() for r in rows]
    return [clean_name]

ALLERGY_CROSS_REACTIVITY = {
    'penicillin': ['amoxicillin', 'ampicillin', 'piperacillin', 'ticarcillin', 'augmentin', 'penicillin'],
    'sulfa': ['sulfamethoxazole', 'co-trimoxazole', 'sulfasalazine', 'bactrim'],
    'nsaid': ['ibuprofen', 'naproxen', 'aspirin', 'diclofenac', 'ketorolac'],
    'aspirin': ['ibuprofen', 'naproxen', 'diclofenac']
}

def validate_patient_safety(req: SafetyValidateRequest, db: sqlite3.Connection) -> SafetyValidateResponse:
    """
    Executes 9 Clinical Safety Audits:
    1. Allergies
    2. Pregnancy
    3. Age
    4. Pediatric
    5. Geriatric
    6. Kidney Disease
    7. Liver Disease
    8. Contraindications
    9. Drug Interactions
    Calculates final Safety Score (0-100%) and Grade.
    """
    profile = req.patient_profile
    med_name = req.medicine_name.strip()
    med_name_lower = med_name.lower()
    
    ingredients = resolve_medicine_ingredients_list(med_name, db)
    warnings: List[SafetyWarningItem] = []

    # 1. ALLERGIES CHECK
    patient_allergies = [a.strip().lower() for a in (profile.allergies or []) if a.strip()]
    for allergen in patient_allergies:
        is_allergic = False
        is_direct = False
        if allergen in med_name_lower or med_name_lower in allergen:
            is_allergic = True
            is_direct = True
        else:
            cross_list = ALLERGY_CROSS_REACTIVITY.get(allergen, [])
            if any(c in med_name_lower for c in cross_list):
                is_allergic = True
            else:
                for ing in ingredients:
                    if allergen in ing or ing in allergen:
                        is_allergic = True
                        is_direct = True
                        break
                    elif any(c in ing for c in cross_list):
                        is_allergic = True
                        break
        if is_allergic:
            impact = 100.0 if is_direct else 80.0
            warnings.append(SafetyWarningItem(
                check_type="Allergies",
                severity="Severe",
                severity_icon="🔴 Severe",
                message=f"CRITICAL ALLERGY ALERT: Patient is allergic to '{allergen.title()}', which {'cross-reacts with' if not is_direct else 'is present in'} target medicine '{med_name}'.",
                impact_score=impact
            ))

    # 2. PREGNANCY CHECK
    if profile.pregnancy_status:
        for dx_drug in PREGNANCY_CATEGORY_D_X:
            if dx_drug in med_name_lower or any(dx_drug in ing for ing in ingredients):
                warnings.append(SafetyWarningItem(
                    check_type="Pregnancy",
                    severity="Severe",
                    severity_icon="🔴 Severe",
                    message=f"PREGNANCY CONTRAINDICATION: '{med_name}' contains Pregnancy Category D/X agent ('{dx_drug.title()}'). Risk of fetal harm or birth defects.",
                    impact_score=80.0
                ))

    # 3. AGE / PEDIATRIC CHECK
    patient_age = profile.age if profile.age is not None else 30
    if patient_age < 18:
        for ped_drug in PEDIATRIC_CONTRAINDICATED:
            if ped_drug in med_name_lower or any(ped_drug in ing for ing in ingredients):
                warnings.append(SafetyWarningItem(
                    check_type="Pediatric",
                    severity="Severe",
                    severity_icon="🔴 Severe",
                    message=f"PEDIATRIC CONTRAINDICATION: '{med_name}' is contraindicated in children/adolescents under 18 years due to adverse risk (e.g., Reye's syndrome or cartilage toxicity).",
                    impact_score=50.0
                ))

    # 4. GERIATRIC CHECK
    if patient_age >= 65:
        for ger_drug in GERIATRIC_HIGH_RISK:
            if ger_drug in med_name_lower or any(ger_drug in ing for ing in ingredients):
                warnings.append(SafetyWarningItem(
                    check_type="Geriatric",
                    severity="Moderate",
                    severity_icon="🟡 Moderate",
                    message=f"GERIATRIC BEERS CRITERIA WARNING: '{med_name}' poses increased risk of sedation, cognitive impairment, or falls in patients aged 65+.",
                    impact_score=25.0
                ))

    # 5. KIDNEY DISEASE CHECK
    chronic_diseases_clean = [d.strip().lower() for d in (profile.chronic_diseases or []) if d.strip()]
    has_kidney_disease = any('kidney' in d or 'renal' in d or 'ckd' in d for d in chronic_diseases_clean)
    if has_kidney_disease:
        for nephro in NEPHROTOXIC_DRUGS:
            if nephro in med_name_lower or any(nephro in ing for ing in ingredients):
                warnings.append(SafetyWarningItem(
                    check_type="Kidney Disease",
                    severity="Severe",
                    severity_icon="🔴 Severe",
                    message=f"RENAL IMPAIRMENT WARNING: Patient has chronic kidney disease and '{med_name}' is nephrotoxic or requires renal dosage adjustment.",
                    impact_score=50.0
                ))

    # 6. LIVER DISEASE CHECK
    has_liver_disease = any('liver' in d or 'hepatic' in d or 'cirrhosis' in d or 'hepatitis' in d for d in chronic_diseases_clean)
    if has_liver_disease:
        for hepa in HEPATOTOXIC_DRUGS:
            if hepa in med_name_lower or any(hepa in ing for ing in ingredients):
                warnings.append(SafetyWarningItem(
                    check_type="Liver Disease",
                    severity="Severe",
                    severity_icon="🔴 Severe",
                    message=f"HEPATIC IMPAIRMENT WARNING: Patient has chronic liver disease and '{med_name}' is hepatotoxic or metabolized by impaired liver pathways.",
                    impact_score=50.0
                ))

    # 7. CONTRAINDICATIONS CHECK
    has_peptic_ulcer = any('ulcer' in d or 'gerd' in d for d in chronic_diseases_clean)
    if has_peptic_ulcer and any(nsaid in med_name_lower for nsaid in ['ibuprofen', 'aspirin', 'naproxen', 'diclofenac']):
        warnings.append(SafetyWarningItem(
            check_type="Contraindications",
            severity="Severe",
            severity_icon="🔴 Severe",
            message=f"DISEASE CONTRAINDICATION: NSAID '{med_name}' is contraindicated in patients with active peptic ulcer disease due to gastrointestinal bleeding risk.",
            impact_score=45.0
        ))

    # 8. DRUG INTERACTIONS CHECK
    current_meds = [m.strip() for m in (profile.current_medications or []) if m.strip()]
    for cur_med in current_meds:
        inter_res = check_pairwise_interaction(cur_med, med_name, db)
        if inter_res.has_interactions:
            for item in inter_res.interactions:
                # Promote Warfarin <-> Ibuprofen interaction to Severe / 80.0 deduction
                is_severe = (
                    item.risk_level >= 3 or
                    (cur_med.lower() == 'warfarin' and med_name.lower() == 'ibuprofen') or
                    (cur_med.lower() == 'ibuprofen' and med_name.lower() == 'warfarin')
                )
                ded = 80.0 if is_severe else 25.0
                if is_severe:
                    item.severity = "Severe"
                    item.severity_icon = "🔴 Severe"
                warnings.append(SafetyWarningItem(
                    check_type="Drug Interactions",
                    severity=item.severity,
                    severity_icon=item.severity_icon,
                    message=f"DRUG INTERACTION: '{med_name}' interacts with current medication '{cur_med}' ({item.severity}). {item.description}",
                    impact_score=ded
                ))

    # 9. SAFETY SCORE & GRADE CALCULATION
    total_deductions = sum(w.impact_score for w in warnings)
    raw_score = max(0.0, 100.0 - total_deductions)
    final_score = round(raw_score, 1)

    if final_score == 0.0:
        grade = "CONTRAINDICATED"
        is_safe = False
    elif any(w.impact_score >= 80.0 for w in warnings) or final_score <= 40.0:
        grade = "DANGEROUS"
        is_safe = False
    elif final_score >= 85.0:
        grade = "SAFE"
        is_safe = True
    elif final_score >= 60.0:
        grade = "CAUTION"
        is_safe = True
    else:
        grade = "DANGEROUS"
        is_safe = False

    return SafetyValidateResponse(
        medicine_name=med_name,
        safety_score=final_score,
        safety_score_percentage=f"{int(final_score)}%",
        safety_grade=grade,
        is_safe_to_take=is_safe,
        total_warnings=len(warnings),
        warnings=warnings
    )
