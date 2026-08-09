"""
AuraMed AI — Emergency Screening Engine
========================================
Hard-stop gate evaluated BEFORE all other clinical reasoning.
If ANY emergency syndrome is detected, the pipeline returns an immediate
RED_URGENT response with targeted emergency advice — no further questions asked.

Priority order: highest-risk syndromes first.
"""
from typing import List, Dict, Any, Optional


class EmergencyPattern:
    def __init__(
        self,
        pattern_id: str,
        name: str,
        keywords: List[str],
        min_match: int,
        advice: str,
        differentials: List[str],
        targeted_questions: List[str],
    ):
        self.pattern_id = pattern_id
        self.name = name
        self.keywords = [k.lower() for k in keywords]
        self.min_match = min_match
        self.advice = advice
        self.differentials = differentials
        self.targeted_questions = targeted_questions

    def match(self, text: str, symptoms: List[str]) -> Optional[Dict[str, Any]]:
        combined = (text + " " + " ".join(symptoms)).lower()
        matched = [k for k in self.keywords if k in combined]
        if len(matched) >= self.min_match:
            return {
                "pattern_id": self.pattern_id,
                "name": self.name,
                "matched_keywords": matched,
                "advice": self.advice,
                "differentials": self.differentials,
                "targeted_questions": self.targeted_questions,
            }
        return None


EMERGENCY_PATTERNS: List[EmergencyPattern] = [
    # 1. STROKE — highest time-sensitivity
    EmergencyPattern(
        "EMRG_STROKE",
        "Acute Stroke / TIA Syndrome",
        ["facial droop", "face drooping", "arm weakness", "leg weakness",
         "slurred speech", "speech difficulty", "sudden numbness", "vision loss", "hemiparesis"],
        min_match=2,
        advice="⚠️ STROKE ALERT: Symptoms are consistent with an acute stroke. Call emergency services (911/112) immediately. Time is critical — every minute counts. Do not drive yourself.",
        differentials=["Acute Ischemic Stroke", "Intracerebral Hemorrhage", "TIA"],
        targeted_questions=[
            "What exact time did the weakness or speech difficulty begin?",
            "Is the weakness on one side of your body only?",
            "Do you have a history of atrial fibrillation or blood clots?",
        ],
    ),

    # 2. ACUTE CORONARY SYNDROME
    EmergencyPattern(
        "EMRG_ACS",
        "Acute Coronary Syndrome",
        ["crushing chest pain", "chest pressure", "chest tightness", "chest pain",
         "pain in arm", "jaw pain", "left arm", "diaphoresis", "cold sweat"],
        min_match=2,
        advice="⚠️ CARDIAC ALERT: These symptoms may indicate a heart attack. Call emergency services immediately. Chew one adult aspirin (325mg) if not allergic and no contraindication. Do not ignore this.",
        differentials=["Acute Myocardial Infarction", "Unstable Angina", "Aortic Dissection"],
        targeted_questions=[
            "Does the chest pain spread to your left arm, neck, or jaw?",
            "Are you sweating, nauseated, or short of breath?",
            "Did the pain start suddenly while at rest?",
        ],
    ),

    # 3. MENINGEAL IRRITATION
    EmergencyPattern(
        "EMRG_MENINGITIS",
        "Meningeal Irritation Syndrome",
        ["neck stiffness", "stiff neck", "nuchal rigidity",
         "photophobia", "light sensitivity", "severe headache", "headache",
         "fever", "high fever", "confusion", "seizure"],
        min_match=3,
        advice="⚠️ MENINGITIS ALERT: The combination of fever, neck stiffness, and headache/photophobia requires immediate emergency evaluation. Bacterial meningitis can be fatal within hours. Go to the emergency room now.",
        differentials=["Bacterial Meningitis", "Viral Meningitis", "Encephalitis", "Subarachnoid Hemorrhage"],
        targeted_questions=[
            "Can you touch your chin to your chest, or does it cause severe pain?",
            "Have you noticed any purple or dark red spots on your skin?",
            "Are you experiencing confusion or unusual drowsiness?",
            "Have you had any seizures?",
        ],
    ),

    # 4. ANAPHYLAXIS
    EmergencyPattern(
        "EMRG_ANAPHYLAXIS",
        "Acute Anaphylaxis",
        ["throat tightening", "throat swelling", "lip swelling", "tongue swelling",
         "stridor", "hives", "urticaria", "wheezing", "difficulty breathing", "allergic reaction"],
        min_match=2,
        advice="⚠️ ANAPHYLAXIS ALERT: This may be a life-threatening allergic reaction. Use epinephrine auto-injector (EpiPen) if available. Call emergency services immediately. Lie flat with legs elevated if dizzy.",
        differentials=["Anaphylactic Shock", "Severe Allergic Reaction", "Angioedema"],
        targeted_questions=[
            "Did this start after eating food, taking a drug, or being stung?",
            "Are your lips, tongue, or throat swelling?",
            "Are you feeling lightheaded or losing consciousness?",
        ],
    ),

    # 5. SUBARACHNOID HEMORRHAGE
    EmergencyPattern(
        "EMRG_SAH",
        "Subarachnoid Hemorrhage (Thunderclap Headache)",
        ["worst headache", "thunderclap headache", "sudden severe headache",
         "headache of my life", "worst headache of my life", "explosive headache"],
        min_match=1,
        advice="⚠️ CRITICAL: A sudden, severe 'worst headache of your life' is a red flag for subarachnoid hemorrhage — a type of brain bleed. This is a medical emergency. Go to the ER immediately.",
        differentials=["Subarachnoid Hemorrhage", "Hypertensive Emergency", "Meningitis"],
        targeted_questions=[
            "Did the headache peak in intensity within seconds?",
            "Do you have neck stiffness or sensitivity to light?",
            "Have you lost consciousness even briefly?",
        ],
    ),

    # 6. RESPIRATORY FAILURE / HYPOXIA
    EmergencyPattern(
        "EMRG_HYPOXIA",
        "Severe Respiratory Failure / Hypoxia",
        ["cannot breathe", "can't breathe", "severe breathing difficulty",
         "oxygen saturation", "spo2 below", "blue lips", "cyanosis", "gasping"],
        min_match=1,
        advice="⚠️ BREATHING EMERGENCY: Severe difficulty breathing requires immediate emergency services. Call 911/112 now. If oxygen is available, use it. Do not leave the patient alone.",
        differentials=["Acute Respiratory Failure", "Pulmonary Embolism", "Severe Asthma", "COPD Exacerbation"],
        targeted_questions=[
            "What is your current oxygen saturation reading if available?",
            "Did this start suddenly or gradually?",
            "Do you have a history of asthma, COPD, or heart failure?",
        ],
    ),

    # 7. DIABETIC KETOACIDOSIS
    EmergencyPattern(
        "EMRG_DKA",
        "Diabetic Ketoacidosis (DKA)",
        ["blood sugar very high", "hyperglycemia", "fruity breath",
         "vomiting", "abdominal pain", "confusion", "rapid breathing"],
        min_match=3,
        advice="⚠️ DKA ALERT: High blood sugar with vomiting and abdominal pain may indicate diabetic ketoacidosis. This is a life-threatening condition. Go to the emergency room immediately.",
        differentials=["Diabetic Ketoacidosis", "Hyperosmolar Hyperglycemic State", "Lactic Acidosis"],
        targeted_questions=[
            "What is your blood glucose level reading?",
            "Do you have a history of diabetes?",
            "Have you been unable to keep fluids down?",
        ],
    ),

    # 8. SUICIDAL IDEATION / PSYCHIATRIC EMERGENCY
    EmergencyPattern(
        "EMRG_SUICIDE",
        "Psychiatric Emergency — Suicidal Ideation",
        ["want to die", "kill myself", "end my life", "suicidal", "suicide",
         "no reason to live", "self-harm", "hurting myself"],
        min_match=1,
        advice="⚠️ MENTAL HEALTH CRISIS: You are not alone. Please contact emergency services or a crisis helpline immediately. National Suicide Hotline (India): iCall 9152987821 | International: 988 (US) | 116 123 (UK).",
        differentials=["Major Depressive Disorder with Suicidal Ideation", "Acute Psychiatric Crisis"],
        targeted_questions=[
            "Are you safe right now?",
            "Do you have a plan or means to harm yourself?",
            "Is there someone with you right now?",
        ],
    ),

    # 9. SEPSIS / SHOCK
    EmergencyPattern(
        "EMRG_SEPSIS",
        "Sepsis / Septic Shock",
        ["very high fever", "low blood pressure", "confusion", "rapid heart rate",
         "cold clammy skin", "not responsive", "unconscious", "sepsis"],
        min_match=3,
        advice="⚠️ SEPSIS ALERT: The combination of high fever, low blood pressure, and confusion may indicate septic shock. This requires immediate emergency care. Call 911/112 now.",
        differentials=["Septic Shock", "Severe Sepsis", "Systemic Inflammatory Response Syndrome"],
        targeted_questions=[
            "What is the blood pressure reading if available?",
            "Is the person confused or difficult to rouse?",
            "Was there a recent infection, surgery, or wound?",
        ],
    ),

    # 10. MASSIVE BLEEDING
    EmergencyPattern(
        "EMRG_BLEEDING",
        "Massive / Uncontrolled Hemorrhage",
        ["heavy bleeding", "bleeding won't stop", "vomiting blood", "coughing blood",
         "blood in stool", "massive blood loss", "hemorrhage"],
        min_match=1,
        advice="⚠️ BLEEDING EMERGENCY: Uncontrolled or severe bleeding is a medical emergency. Apply direct pressure to the wound if external. Call emergency services immediately.",
        differentials=["Upper GI Hemorrhage", "Hemoptysis", "Traumatic Hemorrhage"],
        targeted_questions=[
            "Is the bleeding from a visible wound, mouth, or rectum?",
            "Is the bleeding slowing with pressure, or continuing?",
            "Are you feeling faint, dizzy, or confused?",
        ],
    ),
]


def screen_emergency(query_text: str, symptoms: List[str]) -> Optional[Dict[str, Any]]:
    """
    Evaluates patient input against all emergency patterns.
    Returns the HIGHEST priority match, or None if no emergency detected.
    Priority order matches list order (Stroke → ACS → Meningitis → ...).
    """
    for pattern in EMERGENCY_PATTERNS:
        result = pattern.match(query_text, symptoms)
        if result:
            result["triage"] = "RED_URGENT"
            result["is_emergency"] = True
            return result
    return None
