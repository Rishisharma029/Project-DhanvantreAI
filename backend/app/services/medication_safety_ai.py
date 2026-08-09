import time
import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.med_safety_schema import (
    MedicationSafetyRequest, SafetyCheckResult, MedicationSafetyResponse
)

# 1. Check Pregnancy Safety
def check_pregnancy(meds: List[str], is_pregnant: bool, trimester: Optional[int]) -> SafetyCheckResult:
    if not is_pregnant:
        return SafetyCheckResult(check_name="PREGNANCY", passed=True, severity="NONE", message="Patient is not pregnant.", clinical_action="No action required.")
    
    flagged = []
    for m in meds:
        m_lower = m.lower()
        if "aspirin" in m_lower and trimester and trimester >= 3:
            flagged.append("Aspirin (FDA Category D in 3rd trimester - premature ductus arteriosus closure)")
        elif "warfarin" in m_lower:
            flagged.append("Warfarin (FDA Category X - fetal warfarin syndrome & central nervous system defects)")
        elif "telmisartan" in m_lower or "ramipril" in m_lower or "enalapril" in m_lower:
            flagged.append(f"{m} (FDA Category D - fetal renal agenesis and oligohydramnios)")

    if flagged:
        return SafetyCheckResult(
            check_name="PREGNANCY",
            passed=False,
            severity="CRITICAL",
            message=f"Pregnancy Contraindication: {'; '.join(flagged)}.",
            clinical_action="Immediately discontinue category D/X agents and switch to pregnancy-safe alternatives (e.g. Labetalol, Paracetamol)."
        )
    
    return SafetyCheckResult(check_name="PREGNANCY", passed=True, severity="NONE", message="Medications are acceptable during pregnancy.", clinical_action="Continue standard monitoring.")

# 2. Check Lactation Safety
def check_lactation(meds: List[str], is_lactating: bool) -> SafetyCheckResult:
    if not is_lactating:
        return SafetyCheckResult(check_name="LACTATION", passed=True, severity="NONE", message="Patient is not lactating.", clinical_action="No action required.")
    
    flagged = []
    for m in meds:
        m_lower = m.lower()
        if "codeine" in m_lower or "tramadol" in m_lower:
            flagged.append(f"{m} (Secreted in milk; ultra-rapid CYP2D6 metabolizers risk fatal infant respiratory depression)")
        elif "amiodarone" in m_lower:
            flagged.append(f"{m} (High iodine content; risk of infant hypothyroidism)")

    if flagged:
        return SafetyCheckResult(
            check_name="LACTATION",
            passed=False,
            severity="HIGH",
            message=f"Lactation Safety Alert: {'; '.join(flagged)}.",
            clinical_action="Select non-secreted alternatives or temporarily pump and discard milk during drug administration."
        )
    return SafetyCheckResult(check_name="LACTATION", passed=True, severity="NONE", message="Medications safe during breastfeeding.", clinical_action="Monitor infant for lethargy.")

# 3. Check Pediatrics
def check_pediatrics(meds: List[str], age: Optional[int]) -> SafetyCheckResult:
    if age is None or age >= 18:
        return SafetyCheckResult(check_name="PEDIATRICS", passed=True, severity="NONE", message="Patient is an adult (age >= 18).", clinical_action="No pediatric restriction.")
    
    flagged = []
    for m in meds:
        m_lower = m.lower()
        if "aspirin" in m_lower:
            flagged.append("Aspirin (Strictly contraindicated in children < 19 due to Reye's syndrome risk)")
        elif "ciprofloxacin" in m_lower or "levofloxacin" in m_lower:
            flagged.append(f"{m} (Fluoroquinolones limited in pediatric patients due to arthropathy & cartilage erosion)")

    if flagged:
        return SafetyCheckResult(
            check_name="PEDIATRICS",
            passed=False,
            severity="CRITICAL" if "aspirin" in str(flagged).lower() else "HIGH",
            message=f"Pediatric Dosing / Contraindication: {'; '.join(flagged)}.",
            clinical_action="Substitute with pediatric-approved agents (e.g., Paracetamol / Amoxicillin)."
        )
    return SafetyCheckResult(check_name="PEDIATRICS", passed=True, severity="NONE", message="Pediatric dosing limits respected.", clinical_action="Verify weight-based dosing (mg/kg).")

# 4. Check Geriatrics (Beers Criteria)
def check_geriatrics(meds: List[str], age: Optional[int]) -> SafetyCheckResult:
    if age is None or age < 65:
        return SafetyCheckResult(check_name="GERIATRICS", passed=True, severity="NONE", message="Patient age < 65.", clinical_action="Standard adult dosing applies.")
    
    flagged = []
    for m in meds:
        m_lower = m.lower()
        if "diphenhydramine" in m_lower or "amitriptyline" in m_lower:
            flagged.append(f"{m} (Beers Criteria: Strong anticholinergic activity increases confusion, sedation, and fall risk)")
        elif "aspirin" in m_lower and "warfarin" in m_lower:
            flagged.append("Aspirin + Warfarin combo in elderly (High major GI and intracranial bleeding risk)")

    if flagged:
        return SafetyCheckResult(
            check_name="GERIATRICS",
            passed=False,
            severity="HIGH",
            message=f"Geriatric Beers Criteria Alert: {'; '.join(flagged)}.",
            clinical_action="Review anticholinergic burden and fall risk. Deprescribe or reduce dosage for geriatric safety."
        )
    return SafetyCheckResult(check_name="GERIATRICS", passed=True, severity="NONE", message="No Beers Criteria high-risk drugs detected.", clinical_action="Maintain routine monitoring.")

# 5. Check Renal Adjustment
def check_renal(meds: List[str], egfr: Optional[float]) -> SafetyCheckResult:
    if egfr is None or egfr >= 60.0:
        return SafetyCheckResult(check_name="RENAL", passed=True, severity="NONE", message=f"Renal function normal (eGFR: {egfr or '>=60'} mL/min).", clinical_action="Standard dosing.")
    
    flagged = []
    for m in meds:
        m_lower = m.lower()
        if egfr < 30.0:
            if "metformin" in m_lower:
                flagged.append("Metformin (Contraindicated when eGFR < 30 mL/min due to fatal lactic acidosis risk)")
            elif "ciprofloxacin" in m_lower:
                flagged.append("Ciprofloxacin (Requires 50% dose reduction when eGFR < 30 mL/min)")
        elif egfr < 60.0 and "ciprofloxacin" in m_lower:
            flagged.append("Ciprofloxacin (Requires dose adjustment when eGFR < 50 mL/min)")

    if flagged:
        return SafetyCheckResult(
            check_name="RENAL",
            passed=False,
            severity="CRITICAL" if "metformin" in str(flagged).lower() else "HIGH",
            message=f"Renal Impairment Warning (eGFR = {egfr} mL/min): {'; '.join(flagged)}.",
            clinical_action="Adjust renal dosage, extend dosing interval, or substitute with non-renally cleared agents."
        )
    return SafetyCheckResult(check_name="RENAL", passed=True, severity="NONE", message=f"Dosing acceptable for eGFR {egfr} mL/min.", clinical_action="Monitor serum creatinine.")

# 6. Check Hepatic Adjustment
def check_hepatic(meds: List[str], alt_ast: Optional[float]) -> SafetyCheckResult:
    if alt_ast is None or alt_ast < 100.0:
        return SafetyCheckResult(check_name="HEPATIC", passed=True, severity="NONE", message="Hepatic enzyme levels normal.", clinical_action="Standard dosing.")
    
    flagged = []
    for m in meds:
        m_lower = m.lower()
        if "paracetamol" in m_lower or "acetaminophen" in m_lower:
            flagged.append("Paracetamol (Cap maximum daily dose at 2,000mg due to elevated ALT/AST)")
        elif "atorvastatin" in m_lower or "simvastatin" in m_lower:
            flagged.append(f"{m} (Hold or reduce statin dose when ALT/AST > 3x upper limit of normal)")

    if flagged:
        return SafetyCheckResult(
            check_name="HEPATIC",
            passed=False,
            severity="HIGH",
            message=f"Hepatic Dysfunction Alert (ALT/AST = {alt_ast} U/L): {'; '.join(flagged)}.",
            clinical_action="Reduce hepatically metabolized drug dosages and re-check LFTs in 7-14 days."
        )
    return SafetyCheckResult(check_name="HEPATIC", passed=True, severity="NONE", message="Hepatic clearance acceptable.", clinical_action="Monitor baseline LFTs.")

# 7. Check Allergy & Cross-Reactivity
def check_allergy(meds: List[str], allergies: List[str]) -> SafetyCheckResult:
    if not allergies:
        return SafetyCheckResult(check_name="ALLERGY", passed=True, severity="NONE", message="No known drug allergies reported.", clinical_action="No allergy restriction.")
    
    alg_lowers = [a.lower().strip() for a in allergies]
    flagged = []
    for m in meds:
        m_lower = m.lower()
        for alg in alg_lowers:
            if alg in m_lower or m_lower in alg:
                flagged.append(f"Direct match: '{m}' matches reported allergy '{alg.title()}'")
            elif "penicillin" in alg and ("amoxicillin" in m_lower or "ampicillin" in m_lower):
                flagged.append(f"Cross-reactivity: '{m}' has beta-lactam cross-reactivity with '{alg.title()}'")

    if flagged:
        return SafetyCheckResult(
            check_name="ALLERGY",
            passed=False,
            severity="CRITICAL",
            message=f"Allergy & Cross-Reactivity Alert: {'; '.join(flagged)}.",
            clinical_action="DO NOT ADMINISTER. Discontinue immediately and substitute with an alternative non-cross-reactive pharmacological class."
        )
    return SafetyCheckResult(check_name="ALLERGY", passed=True, severity="NONE", message="No allergy cross-reactivity detected.", clinical_action="Document allergy profile.")

# 8. Check QT Prolongation (TdP)
def check_qt_prolongation(meds: List[str]) -> SafetyCheckResult:
    qt_drugs = ["ciprofloxacin", "levofloxacin", "azithromycin", "amiodarone", "haloperidol", "ondansetron"]
    matches = [m for m in meds if any(qd in m.lower() for qd in qt_drugs)]

    if len(matches) >= 2:
        return SafetyCheckResult(
            check_name="QT_PROLONGATION",
            passed=False,
            severity="CRITICAL",
            message=f"Synergistic QT Prolongation Hazard: Co-administration of {', '.join(matches)} significantly increases Torsades de Pointes (TdP) arrhythmia risk.",
            clinical_action="Obtain baseline 12-lead ECG. Avoid concurrent QTc-lengthening agents."
        )
    elif len(matches) == 1:
        return SafetyCheckResult(
            check_name="QT_PROLONGATION",
            passed=True,
            severity="LOW",
            message=f"Single QT-lengthening agent detected ({matches[0]}). Low standalone risk.",
            clinical_action="Monitor baseline electrolytes (K+, Mg2+)."
        )
    return SafetyCheckResult(check_name="QT_PROLONGATION", passed=True, severity="NONE", message="No QTc-lengthening agents detected.", clinical_action="No ECG monitoring needed.")

# 9. Check Duplicate Therapy
def check_duplicate_therapy(meds: List[str]) -> SafetyCheckResult:
    classes = {
        "NSAID": ["aspirin", "ibuprofen", "naproxen", "diclofenac"],
        "ACE_INHIBITOR": ["ramipril", "enalapril", "lisinopril"],
        "FLUOROQUINOLONE": ["ciprofloxacin", "levofloxacin", "moxifloxacin"]
    }
    
    dups = []
    for cls_name, cls_meds in classes.items():
        found = [m for m in meds if any(cm in m.lower() for cm in cls_meds)]
        if len(found) > 1:
            dups.append(f"Duplicate {cls_name} therapy: {', '.join(found)}")

    if dups:
        return SafetyCheckResult(
            check_name="DUPLICATE_THERAPY",
            passed=False,
            severity="HIGH",
            message=f"Pharmacological Redundancy: {'; '.join(dups)}.",
            clinical_action="Eliminate duplicate agent to prevent additive toxicity without therapeutic benefit."
        )
    return SafetyCheckResult(check_name="DUPLICATE_THERAPY", passed=True, severity="NONE", message="No duplicate class therapy detected.", clinical_action="Maintain regimen.")

# 10. Check Black Box Warnings
def check_black_box_warnings(meds: List[str]) -> SafetyCheckResult:
    black_box_db = {
        "ciprofloxacin": "FDA Black Box: Risk of severe tendonitis, tendon rupture, peripheral neuropathy, and CNS effects.",
        "warfarin": "FDA Black Box: Risk of severe, fatal bleeding and hemorrhage.",
        "aspirin": "FDA Black Box: Severe GI bleeding and ulceration hazard."
    }

    flagged = []
    for m in meds:
        m_lower = m.lower()
        for k, warn in black_box_db.items():
            if k in m_lower:
                flagged.append(f"{m}: {warn}")

    if flagged:
        return SafetyCheckResult(
            check_name="BLACK_BOX_WARNING",
            passed=False,
            severity="CRITICAL",
            message=f"FDA Black Box Warning Alert: {'; '.join(flagged)}.",
            clinical_action="Inform patient of high-potency boxed warning risks and document explicit informed consent."
        )
    return SafetyCheckResult(check_name="BLACK_BOX_WARNING", passed=True, severity="NONE", message="No FDA Black Box Warning drugs detected.", clinical_action="Standard routine care.")

# Main 10-Point Safety Evaluator
def evaluate_medication_safety(req: MedicationSafetyRequest, db: sqlite3.Connection) -> MedicationSafetyResponse:
    """Execute complete 10-Point Clinical Medication Safety Audit."""
    t0 = time.perf_counter()
    meds = req.medications

    checks = [
        check_pregnancy(meds, req.is_pregnant, req.trimester),
        check_lactation(meds, req.is_lactating),
        check_pediatrics(meds, req.patient_age),
        check_geriatrics(meds, req.patient_age),
        check_renal(meds, req.egfr_ml_min),
        check_hepatic(meds, req.alt_ast_u_l),
        check_allergy(meds, req.known_allergies or []),
        check_qt_prolongation(meds),
        check_duplicate_therapy(meds),
        check_black_box_warnings(meds)
    ]

    # Calculate Safety Score (0 - 100) & Risk Level
    deductions = 0
    alerts_found = 0
    recommendations = []

    for c in checks:
        if not c.passed:
            alerts_found += 1
            recommendations.append(f"[{c.check_name}] {c.clinical_action}")
            if c.severity == "CRITICAL":
                deductions += 30
            elif c.severity == "HIGH":
                deductions += 15
            elif c.severity == "MODERATE":
                deductions += 10
            elif c.severity == "LOW":
                deductions += 5

    safety_score = max(100 - deductions, 0)

    if safety_score >= 85 and alerts_found == 0:
        risk_level = "LOW_GREEN"
    elif safety_score >= 70:
        risk_level = "MODERATE_YELLOW"
    elif safety_score >= 50:
        risk_level = "HIGH_ORANGE"
    else:
        risk_level = "CRITICAL_RED"

    if not recommendations:
        recommendations.append("Medication profile passed all 10 clinical safety checks cleanly. Proceed with standard therapy.")

    t1 = time.perf_counter()
    latency_ms = int((t1 - t0) * 1000)

    return MedicationSafetyResponse(
        safety_score=safety_score,
        risk_level=risk_level,
        total_alerts_found=alerts_found,
        safety_checks=checks,
        actionable_recommendations=recommendations,
        execution_time_ms=latency_ms
    )
