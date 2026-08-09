from typing import Optional, List, Dict, Any
from app.schemas.scoring_schema import ScoringResult

def calculate_curb65(confusion: bool, urea_mmol: Optional[float], rr: Optional[int],
                     systolic_bp: Optional[int], diastolic_bp: Optional[int], age: int) -> ScoringResult:
    score = 0
    if confusion: score += 1
    if urea_mmol is not None and urea_mmol > 7: score += 1
    if rr is not None and rr >= 30: score += 1
    if systolic_bp is not None and diastolic_bp is not None:
        if systolic_bp < 90 or diastolic_bp <= 60: score += 1
    if age >= 65: score += 1
    
    risk = "Low risk (outpatient)"
    action = "Consider outpatient management"
    if score == 2:
        risk = "Moderate risk"
        action = "Consider hospital admission"
    elif score >= 3:
        risk = "High risk"
        action = "Admit to hospital, consider ICU assessment"
        
    return ScoringResult(
        score=score,
        max_score=5,
        risk_category=risk,
        clinical_action=action,
        explanation=f"CURB-65 score of {score}. Assessed C, U, R, B, and Age 65 parameters.",
        score_name="CURB-65"
    )

def calculate_news2(spo2_scale: int, spo2: int, supplemental_o2: bool, 
                    systolic_bp: int, pulse_rate: int, consciousness: str, 
                    temp: float, rr: int) -> ScoringResult:
    score = 0
    
    # RR
    if rr <= 8 or rr >= 25: score += 3
    elif rr >= 21: score += 2
    elif rr <= 11: score += 1
    
    # SpO2
    if spo2_scale == 1:
        if spo2 <= 91: score += 3
        elif spo2 <= 93: score += 2
        elif spo2 <= 95: score += 1
    else: # scale 2
        if spo2 <= 83 or (spo2 >= 97 and supplemental_o2): score += 3
        elif spo2 <= 85 or (spo2 >= 95 and supplemental_o2): score += 2
        elif spo2 <= 87 or (spo2 >= 93 and supplemental_o2): score += 1
        
    if supplemental_o2: score += 2
    
    # SBP
    if systolic_bp <= 90 or systolic_bp >= 220: score += 3
    elif systolic_bp <= 100: score += 2
    elif systolic_bp <= 110: score += 1
    
    # Pulse
    if pulse_rate <= 40 or pulse_rate >= 131: score += 3
    elif pulse_rate >= 111: score += 2
    elif pulse_rate <= 50 or pulse_rate >= 91: score += 1
    
    # Consciousness (ACVPU)
    if consciousness.upper() in ["V", "P", "U", "C"]: score += 3
    
    # Temp
    if temp <= 35.0 or temp >= 39.1: score += 2
    elif temp <= 36.0 or temp >= 38.1: score += 1
    
    risk = "Low risk"
    action = "Ward-based response"
    if score >= 7:
        risk = "High risk"
        action = "High-level emergency response, critical care assessment"
    elif score >= 5:
        risk = "Medium risk"
        action = "Urgent response, medical team review"
        
    return ScoringResult(
        score=score,
        max_score=20,
        risk_category=risk,
        clinical_action=action,
        explanation=f"NEWS2 score of {score}.",
        score_name="NEWS2"
    )

def calculate_qsofa(altered_mental_status: bool, rr: int, systolic_bp: int) -> ScoringResult:
    score = 0
    if altered_mental_status: score += 1
    if rr >= 22: score += 1
    if systolic_bp <= 100: score += 1
    
    risk = "Low risk"
    action = "Continue standard management"
    if score >= 2:
        risk = "High risk for sepsis"
        action = "Investigate further, consider sepsis protocols"
        
    return ScoringResult(
        score=score,
        max_score=3,
        risk_category=risk,
        clinical_action=action,
        explanation=f"qSOFA score of {score}.",
        score_name="qSOFA"
    )

def calculate_wells_pe(clinical_signs_dvt: bool, pe_most_likely: bool, heart_rate: int,
                       immobilisation: bool, prev_pe_dvt: bool, haemoptysis: bool, malignancy: bool) -> ScoringResult:
    score = 0.0
    if clinical_signs_dvt: score += 3.0
    if pe_most_likely: score += 3.0
    if heart_rate > 100: score += 1.5
    if immobilisation: score += 1.5
    if prev_pe_dvt: score += 1.5
    if haemoptysis: score += 1.0
    if malignancy: score += 1.0
    
    risk = "Low probability"
    action = "Consider D-dimer (or PERC rule)"
    if score > 4.0:
        risk = "High probability"
        action = "Proceed directly to CTPA"
        
    return ScoringResult(
        score=score,
        max_score=12.5,
        risk_category=risk,
        clinical_action=action,
        explanation=f"Wells PE score of {score}.",
        score_name="Wells Score for PE"
    )

def calculate_heart_score(history: int, ecg: int, age: int, risk_factors: int, troponin: int) -> ScoringResult:
    # Variables expected as 0, 1, or 2 based on HEART scale
    score = history + ecg + risk_factors + troponin
    
    if age >= 65: score += 2
    elif age >= 45: score += 1
    
    risk = "Low risk"
    action = "Consider early discharge"
    if score >= 7:
        risk = "High risk"
        action = "Early invasive strategy"
    elif score >= 4:
        risk = "Moderate risk"
        action = "Observation, serial testing"
        
    return ScoringResult(
        score=score,
        max_score=10,
        risk_category=risk,
        clinical_action=action,
        explanation=f"HEART score of {score}.",
        score_name="HEART Score"
    )

def calculate_cha2ds2_vasc(chf: bool, hypertension: bool, age: int, diabetes: bool,
                           stroke_tia: bool, vascular_disease: bool, female_sex: bool) -> ScoringResult:
    score = 0
    if chf: score += 1
    if hypertension: score += 1
    if age >= 75: score += 2
    elif age >= 65: score += 1
    if diabetes: score += 1
    if stroke_tia: score += 2
    if vascular_disease: score += 1
    if female_sex: score += 1
    
    risk = "Low risk"
    action = "No anticoagulation typically required"
    if score >= 2:
        risk = "High risk"
        action = "Anticoagulate"
    elif score == 1:
        risk = "Intermediate risk"
        action = "Consider anticoagulation"
        
    return ScoringResult(
        score=score,
        max_score=9,
        risk_category=risk,
        clinical_action=action,
        explanation=f"CHA2DS2-VASc score of {score}.",
        score_name="CHA2DS2-VASc"
    )

def calculate_centor(exudate: bool, lymphadenopathy: bool, fever: bool, cough: bool) -> ScoringResult:
    score = 0
    if exudate: score += 1
    if lymphadenopathy: score += 1
    if fever: score += 1
    if not cough: score += 1
    
    risk = "Low probability"
    action = "No antibiotics"
    if score == 4:
        risk = "High probability"
        action = "Empiric antibiotics"
    elif score >= 2:
        risk = "Moderate probability"
        action = "Consider throat swab/rapid test"
        
    return ScoringResult(
        score=score,
        max_score=4,
        risk_category=risk,
        clinical_action=action,
        explanation=f"Centor score of {score}.",
        score_name="Centor Score"
    )

def calculate_gcs(eyes: int, verbal: int, motor: int) -> ScoringResult:
    score = eyes + verbal + motor
    
    risk = "Normal"
    action = "Monitor"
    if score <= 8:
        risk = "Severe"
        action = "Intubate (GCS <= 8)"
    elif score <= 12:
        risk = "Moderate"
        action = "Close observation, consider imaging"
    elif score <= 14:
        risk = "Mild"
        action = "Monitor closely"
        
    return ScoringResult(
        score=score,
        max_score=15,
        risk_category=risk,
        clinical_action=action,
        explanation=f"GCS score of {score} (E{eyes} V{verbal} M{motor}).",
        score_name="GCS"
    )

def calculate_score(score_name: str, patient_data: dict) -> Optional[ScoringResult]:
    """Calculates whichever clinical score is appropriate given the data available."""
    if score_name == "CURB-65":
        return calculate_curb65(
            patient_data.get("confusion", False),
            patient_data.get("urea_mmol"),
            patient_data.get("rr"),
            patient_data.get("systolic_bp"),
            patient_data.get("diastolic_bp"),
            patient_data.get("age", 0)
        )
    elif score_name == "NEWS2":
        return calculate_news2(
            patient_data.get("spo2_scale", 1),
            patient_data.get("spo2", 98),
            patient_data.get("supplemental_o2", False),
            patient_data.get("systolic_bp", 120),
            patient_data.get("pulse_rate", 70),
            patient_data.get("consciousness", "A"),
            patient_data.get("temp", 37.0),
            patient_data.get("rr", 16)
        )
    elif score_name == "qSOFA":
        return calculate_qsofa(
            patient_data.get("altered_mental_status", False),
            patient_data.get("rr", 16),
            patient_data.get("systolic_bp", 120)
        )
    elif score_name == "Wells Score for PE":
        return calculate_wells_pe(
            patient_data.get("clinical_signs_dvt", False),
            patient_data.get("pe_most_likely", False),
            patient_data.get("heart_rate", 80),
            patient_data.get("immobilisation", False),
            patient_data.get("prev_pe_dvt", False),
            patient_data.get("haemoptysis", False),
            patient_data.get("malignancy", False)
        )
    elif score_name == "HEART Score":
        return calculate_heart_score(
            patient_data.get("history", 0),
            patient_data.get("ecg", 0),
            patient_data.get("age", 0),
            patient_data.get("risk_factors", 0),
            patient_data.get("troponin", 0)
        )
    elif score_name == "CHA2DS2-VASc":
        return calculate_cha2ds2_vasc(
            patient_data.get("chf", False),
            patient_data.get("hypertension", False),
            patient_data.get("age", 0),
            patient_data.get("diabetes", False),
            patient_data.get("stroke_tia", False),
            patient_data.get("vascular_disease", False),
            patient_data.get("female_sex", False)
        )
    elif score_name == "Centor Score":
        return calculate_centor(
            patient_data.get("exudate", False),
            patient_data.get("lymphadenopathy", False),
            patient_data.get("fever", False),
            patient_data.get("cough", True)
        )
    elif score_name == "GCS":
        return calculate_gcs(
            patient_data.get("eyes", 4),
            patient_data.get("verbal", 5),
            patient_data.get("motor", 6)
        )
    return None

def get_applicable_scores(diagnosis: str, available_data: dict) -> List[str]:
    """Returns which scoring systems are applicable for a given diagnosis."""
    mapping = {
        "Community-Acquired Pneumonia": ["CURB-65", "NEWS2", "qSOFA"],
        "Sepsis": ["qSOFA", "NEWS2"],
        "Pulmonary Embolism": ["Wells Score for PE", "NEWS2"],
        "NSTEMI": ["HEART Score", "NEWS2"],
        "Unstable Angina": ["HEART Score"],
        "Atrial Fibrillation": ["CHA2DS2-VASc"],
        "Pharyngitis": ["Centor Score"],
        "Head Injury": ["GCS"],
        "Trauma": ["GCS", "NEWS2"]
    }
    # Simplified logic: match diagnosis directly, ignore data completeness for now
    applicable = mapping.get(diagnosis, ["NEWS2"]) # Default to NEWS2
    return applicable
