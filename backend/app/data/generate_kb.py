import os
import random

specialties = {
    "Emergency": [
        "Trauma", "Anaphylaxis", "Sepsis", "Shock", "Acute Poisoning", 
        "Burns", "Cardiac Arrest", "Hypothermia", "Heat Stroke", "Polytrauma",
        "Acute Respiratory Failure", "Hypertensive Emergency", "Acute Abdomen", "Hemorrhage", "Status Epilepticus"
    ],
    "Respiratory": [
        "Asthma Exacerbation", "COPD Exacerbation", "Pneumonia", "Pulmonary Embolism", "Pneumothorax",
        "Acute Bronchitis", "Tuberculosis", "Pleural Effusion", "ARDS", "Lung Cancer",
        "Bronchiectasis", "Interstitial Lung Disease", "Cystic Fibrosis", "Pulmonary Hypertension", "Sleep Apnea"
    ],
    "Cardiology": [
        "Acute Coronary Syndrome", "Heart Failure", "Arrhythmia", "Pericarditis", "Myocarditis",
        "Aortic Dissection", "Endocarditis", "Valvular Heart Disease", "Atrial Fibrillation", "Cardiomyopathy",
        "Angina Pectoris", "Cardiac Tamponade", "Peripheral Artery Disease", "Deep Vein Thrombosis", "Cor Pulmonale"
    ],
    "Neurology": [
        "Meningitis", "Stroke", "TIA", "Migraine", "Seizure Disorder",
        "Multiple Sclerosis", "Parkinsons", "Guillain Barre", "Myasthenia Gravis", "ALS",
        "Encephalitis", "Subarachnoid Hemorrhage", "Dementia", "Neuropathy", "Brain Tumor"
    ],
    "Gastroenterology": [
        "Appendicitis", "Pancreatitis", "Cholecystitis", "Peptic Ulcer Disease", "Gastroenteritis",
        "IBD", "IBS", "Liver Cirrhosis", "Hepatitis", "GI Bleed",
        "Bowel Obstruction", "GERD", "Celiac Disease", "Diverticulitis", "Esophageal Varices"
    ],
    "Urology": [
        "UTI", "Kidney Stones", "Pyelonephritis", "BPH", "Prostatitis"
    ],
    "Endocrinology": [
        "DKA", "Hypoglycemia", "Hyperthyroidism", "Hypothyroidism", "Addisons Disease"
    ],
    "Dermatology": [
        "Cellulitis", "Psoriasis", "Eczema", "Melanoma", "Stevens Johnson Syndrome"
    ],
    "Obstetrics/Gynecology": [
        "Ectopic Pregnancy", "Preeclampsia", "Placenta Previa", "Placental Abruption", "PID",
        "Endometriosis", "PCOS", "Ovarian Torsion", "Fibroids", "Postpartum Hemorrhage"
    ]
}

entries = []
count = 1

for spec, diseases in specialties.items():
    for disease in diseases:
        d_clean = disease.upper().replace(' ', '_').replace('/', '_').replace('-', '_').replace("'", '')
        syn_id = f"SYN_{d_clean}"
        
        is_emergent = (spec == "Emergency") or ("ACUTE" in d_clean) or (disease in ["Stroke", "Aortic Dissection", "Ectopic Pregnancy", "Testicular Torsion", "Status Epilepticus", "Sepsis", "Anaphylaxis", "Cardiac Arrest", "DKA"])
        
        triage = "RED_URGENT" if is_emergent else "YELLOW_MODERATE"
        priority = 100 if is_emergent else random.randint(50, 89)
        
        entry = f"""    {{
        "syndrome_id": "{syn_id}",
        "name": "{disease} Syndrome",
        "specialty": "{spec}",
        "required_keywords": ["{disease.lower()}", "pain", "symptom"],
        "supporting_findings": ["fatigue", "weakness"],
        "excluded_findings": ["chronic", "weeks", "months"],
        "red_flags": ["severe", "sudden", "unresponsive"],
        "min_match_count": 1,
        "triage": "{triage}",
        "is_emergency": {"True" if is_emergent else "False"},
        "priority": {priority},
        "differentials": [
            {{"disease_name": "{disease}", "probability": 0.85, "status": "RULED_IN", "icd11_code": "XXXX", "supporting": ["Classic signs"], "missing": ["Lab confirmation"]}}
        ],
        "recommended_investigations": ["Blood Test", "Imaging"],
        "targeted_questions": [
            "When did the symptoms start?",
            "Is the pain severe?"
        ],
        "question_category": "{spec}"
    }}"""
        entries.append(entry)
        count += 1

# Make sure we have 100
assert len(entries) == 100, f"Expected 100, got {len(entries)}"

file_content = "SYNDROME_KB = [\n" + ",\n".join(entries) + "\n]\n"

out_path = r"c:\Users\Rishi Sharma\OneDrive\Desktop\PRODUCTION\medical idea\backend\app\data\syndrome_kb.py"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(file_content)

print(f"Generated {len(entries)} entries in {out_path}")
