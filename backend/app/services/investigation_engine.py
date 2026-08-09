from typing import List, Optional, Dict, Any
from app.schemas.investigation_schema import InvestigationItem, InvestigationMap

INVESTIGATION_MAP = {
    "Community-Acquired Pneumonia": {
        "first_line": [
            {"test": "Chest X-Ray (CXR)", "rationale": "Confirm consolidation / lobar infiltrate", "urgency": "URGENT"},
            {"test": "CBC + Differential", "rationale": "Leukocytosis suggests bacterial cause", "urgency": "ROUTINE"},
            {"test": "CRP", "rationale": "Inflammatory marker for severity", "urgency": "ROUTINE"},
            {"test": "Blood culture x2", "rationale": "Before antibiotics in severe CAP", "urgency": "URGENT"},
            {"test": "Sputum culture", "rationale": "Identify organism and sensitivities", "urgency": "ROUTINE"},
            {"test": "Urine Legionella antigen", "rationale": "CURB-65 >= 2 or severe CAP", "urgency": "ROUTINE"},
            {"test": "Urine Pneumococcal antigen", "rationale": "Severe CAP", "urgency": "ROUTINE"},
        ],
        "second_line": [
            {"test": "Procalcitonin", "rationale": "Bacterial vs viral differentiation", "urgency": "ROUTINE"},
            {"test": "CT Thorax", "rationale": "If CXR equivocal or no improvement", "urgency": "NON-URGENT"},
            {"test": "Thoracocentesis", "rationale": "If pleural effusion present", "urgency": "URGENT"},
        ],
        "scoring_systems": ["CURB-65", "PSI"],
        "guideline": "BTS CAP Guidelines 2023 | NICE NG138"
    },
    "Bacterial Meningitis": {
        "first_line": [
            {"test": "Lumbar Puncture (CSF)", "rationale": "Cell count, protein, glucose, culture", "urgency": "EMERGENCY"},
            {"test": "Blood cultures", "rationale": "Identify pathogen", "urgency": "URGENT"},
            {"test": "CT Head", "rationale": "Rule out raised ICP before LP if indicated", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Meningitis guidelines"
    },
    "Viral Meningitis": {
         "first_line": [
            {"test": "Lumbar Puncture (CSF PCR)", "rationale": "Viral panel", "urgency": "URGENT"}
         ],
         "second_line": [],
         "scoring_systems": [],
         "guideline": "Viral Meningitis guidelines"
    },
    "Encephalitis": {
         "first_line": [
            {"test": "MRI Brain", "rationale": "Detect temporal lobe changes for HSV", "urgency": "URGENT"},
            {"test": "Lumbar Puncture (CSF PCR)", "rationale": "HSV PCR", "urgency": "URGENT"}
         ],
         "second_line": [],
         "scoring_systems": [],
         "guideline": "Encephalitis guidelines"
    },
    "SAH": {
         "first_line": [
            {"test": "CT Head (non-contrast)", "rationale": "Detect acute blood", "urgency": "EMERGENCY"},
            {"test": "Lumbar Puncture", "rationale": "Xanthochromia if CT negative and high suspicion", "urgency": "URGENT"}
         ],
         "second_line": [
             {"test": "CT Angiogram", "rationale": "Detect aneurysm", "urgency": "URGENT"}
         ],
         "scoring_systems": ["WFNS", "Fisher Grade"],
         "guideline": "SAH guidelines"
    },
    "STEMI": {
        "first_line": [
            {"test": "12-lead ECG", "rationale": "Detect ST elevation", "urgency": "EMERGENCY"},
            {"test": "Coronary Angiography", "rationale": "For PCI", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["TIMI", "GRACE"],
        "guideline": "AHA/ACC STEMI guidelines"
    },
    "NSTEMI": {
        "first_line": [
            {"test": "12-lead ECG", "rationale": "Ischemic changes", "urgency": "URGENT"},
            {"test": "High-sensitivity Troponin", "rationale": "Detect myocardial injury", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["TIMI", "GRACE", "HEART Score"],
        "guideline": "AHA/ACC NSTEMI guidelines"
    },
    "Unstable Angina": {
        "first_line": [
            {"test": "12-lead ECG", "rationale": "Ischemic changes", "urgency": "URGENT"},
            {"test": "High-sensitivity Troponin", "rationale": "Rule out MI", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["HEART Score"],
        "guideline": "AHA/ACC NSTEMI guidelines"
    },
    "Aortic Dissection": {
        "first_line": [
            {"test": "CT Angiogram Thorax/Abdomen", "rationale": "Gold standard for dissection flap", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Aortic Dissection guidelines"
    },
    "Heart Failure": {
        "first_line": [
            {"test": "BNP / NT-proBNP", "rationale": "Marker of ventricular stretch", "urgency": "URGENT"},
            {"test": "Echocardiogram", "rationale": "Assess LV function", "urgency": "URGENT"},
            {"test": "Chest X-Ray", "rationale": "Assess for pulmonary edema", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["NYHA"],
        "guideline": "Heart Failure guidelines"
    },
    "Pericarditis": {
        "first_line": [
            {"test": "12-lead ECG", "rationale": "Widespread PR depression / ST elevation", "urgency": "URGENT"},
            {"test": "Echocardiogram", "rationale": "Check for pericardial effusion", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Pericarditis guidelines"
    },
    "Infective Endocarditis": {
        "first_line": [
            {"test": "Blood cultures x3", "rationale": "Identify pathogen", "urgency": "URGENT"},
            {"test": "Echocardiogram", "rationale": "Check for vegetations (TTE then TEE)", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["Duke Criteria"],
        "guideline": "Infective Endocarditis guidelines"
    },
    "COPD Exacerbation": {
        "first_line": [
            {"test": "ABG", "rationale": "Assess for type 2 respiratory failure", "urgency": "URGENT"},
            {"test": "Chest X-Ray", "rationale": "Rule out pneumonia/pneumothorax", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "GOLD guidelines"
    },
    "Pulmonary Embolism": {
        "first_line": [
            {"test": "CTPA", "rationale": "Diagnostic imaging of choice", "urgency": "URGENT"},
            {"test": "D-dimer", "rationale": "Rule out if low risk", "urgency": "URGENT"},
        ],
        "second_line": [
            {"test": "V/Q Scan", "rationale": "If CTPA contraindicated", "urgency": "URGENT"}
        ],
        "scoring_systems": ["Wells Score for PE", "PERC"],
        "guideline": "PE guidelines"
    },
    "Asthma Exacerbation": {
        "first_line": [
            {"test": "PEFR", "rationale": "Assess severity", "urgency": "URGENT"},
            {"test": "ABG", "rationale": "If life-threatening features", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "BTS Asthma guidelines"
    },
    "Pneumothorax": {
        "first_line": [
            {"test": "Chest X-Ray", "rationale": "Identify pleural line", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Pneumothorax guidelines"
    },
    "Pleural Effusion": {
        "first_line": [
            {"test": "Chest X-Ray", "rationale": "Blunting of costophrenic angle", "urgency": "ROUTINE"},
            {"test": "Pleural fluid analysis", "rationale": "Light's criteria (protein, LDH, cytology, culture)", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["Light's Criteria"],
        "guideline": "Pleural Effusion guidelines"
    },
    "Tuberculosis": {
        "first_line": [
            {"test": "Chest X-Ray", "rationale": "Apical consolidation / cavitation", "urgency": "ROUTINE"},
            {"test": "Sputum AFB smear and culture x3", "rationale": "Identify mycobacteria", "urgency": "ROUTINE"},
        ],
        "second_line": [
            {"test": "IGRA", "rationale": "Latent TB testing", "urgency": "ROUTINE"}
        ],
        "scoring_systems": [],
        "guideline": "TB guidelines"
    },
    "Appendicitis": {
        "first_line": [
            {"test": "Ultrasound Abdomen", "rationale": "First line in children/young adults", "urgency": "URGENT"},
            {"test": "CT Abdomen/Pelvis", "rationale": "Highest sensitivity/specificity", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["Alvarado Score"],
        "guideline": "Appendicitis guidelines"
    },
    "Cholecystitis": {
        "first_line": [
            {"test": "Ultrasound Abdomen", "rationale": "Gallstones, gallbladder wall thickening", "urgency": "URGENT"},
            {"test": "LFTs", "rationale": "Check for biliary obstruction", "urgency": "URGENT"},
        ],
        "second_line": [
            {"test": "MRCP", "rationale": "If suspicion of CBD stones", "urgency": "ROUTINE"}
        ],
        "scoring_systems": [],
        "guideline": "Tokyo Guidelines"
    },
    "Pancreatitis": {
        "first_line": [
            {"test": "Lipase", "rationale": ">3x upper limit of normal", "urgency": "URGENT"},
            {"test": "Ultrasound Abdomen", "rationale": "Check for gallstones", "urgency": "URGENT"},
        ],
        "second_line": [
            {"test": "CT Abdomen", "rationale": "Assess for necrosis/complications", "urgency": "ROUTINE"}
        ],
        "scoring_systems": ["Glasgow Score", "Ranson Criteria"],
        "guideline": "Acute Pancreatitis guidelines"
    },
    "Upper GI Bleed": {
        "first_line": [
            {"test": "FBC, U&E, LFT, Coagulation", "rationale": "Assess Hb and baseline", "urgency": "URGENT"},
            {"test": "OGD (Endoscopy)", "rationale": "Diagnostic and therapeutic", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["Glasgow-Blatchford Score", "Rockall Score"],
        "guideline": "UGIB guidelines"
    },
    "Lower GI Bleed": {
        "first_line": [
            {"test": "FBC, Coagulation", "rationale": "Assess Hb", "urgency": "URGENT"},
            {"test": "Colonoscopy", "rationale": "Diagnostic and therapeutic", "urgency": "URGENT"},
        ],
        "second_line": [
            {"test": "CT Angiogram", "rationale": "If massive bleeding", "urgency": "EMERGENCY"}
        ],
        "scoring_systems": [],
        "guideline": "LGIB guidelines"
    },
    "Peritonitis": {
        "first_line": [
            {"test": "Erect Chest X-Ray", "rationale": "Pneumoperitoneum", "urgency": "EMERGENCY"},
            {"test": "CT Abdomen", "rationale": "Identify source of perforation", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Peritonitis guidelines"
    },
    "Bowel Obstruction": {
        "first_line": [
            {"test": "CT Abdomen/Pelvis", "rationale": "Identify transition point", "urgency": "URGENT"},
            {"test": "Abdominal X-Ray", "rationale": "Dilated loops of bowel", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Bowel Obstruction guidelines"
    },
    "Ischaemic Colitis": {
        "first_line": [
            {"test": "CT Abdomen with contrast", "rationale": "Bowel wall thickening/pneumatosis", "urgency": "EMERGENCY"},
            {"test": "Lactate", "rationale": "Marker of ischemia", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Ischaemic Colitis guidelines"
    },
    "DKA": {
        "first_line": [
            {"test": "Capillary Blood Glucose", "rationale": ">11 mmol/L", "urgency": "EMERGENCY"},
            {"test": "Capillary/Urine Ketones", "rationale": "Elevated", "urgency": "EMERGENCY"},
            {"test": "VBG", "rationale": "pH < 7.3, Bicarbonate < 15", "urgency": "EMERGENCY"},
            {"test": "U&E", "rationale": "Check Potassium", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "JBDS DKA Guidelines"
    },
    "HHS": {
        "first_line": [
            {"test": "Blood Glucose", "rationale": ">30 mmol/L", "urgency": "EMERGENCY"},
            {"test": "Serum Osmolality", "rationale": ">320 mOsm/kg", "urgency": "EMERGENCY"},
            {"test": "U&E", "rationale": "Significant dehydration", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "JBDS HHS Guidelines"
    },
    "Hypoglycaemia": {
        "first_line": [
            {"test": "Capillary Blood Glucose", "rationale": "<4.0 mmol/L", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Hypoglycaemia guidelines"
    },
    "Thyroid Storm": {
        "first_line": [
            {"test": "TFTs", "rationale": "High T3/T4, Low TSH", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["Burch-Wartofsky Point Scale"],
        "guideline": "Thyroid Storm guidelines"
    },
    "Adrenal Crisis": {
        "first_line": [
            {"test": "Random Cortisol", "rationale": "Appropriately low", "urgency": "EMERGENCY"},
            {"test": "U&E", "rationale": "Hyponatremia, Hyperkalemia", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Adrenal Crisis guidelines"
    },
    "Sepsis": {
        "first_line": [
            {"test": "Lactate", "rationale": "Tissue hypoperfusion", "urgency": "URGENT"},
            {"test": "Blood cultures", "rationale": "Before antibiotics", "urgency": "URGENT"},
            {"test": "FBC, CRP", "rationale": "Infection markers", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["qSOFA", "NEWS2", "SIRS"],
        "guideline": "Surviving Sepsis Campaign"
    },
    "Septic Shock": {
        "first_line": [
            {"test": "Lactate", "rationale": "Tissue hypoperfusion", "urgency": "EMERGENCY"},
            {"test": "Blood cultures", "rationale": "Before antibiotics", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["qSOFA", "NEWS2"],
        "guideline": "Surviving Sepsis Campaign"
    },
    "UTI": {
        "first_line": [
            {"test": "Urine Dipstick", "rationale": "Nitrites and Leukocytes", "urgency": "ROUTINE"},
            {"test": "Urine MCS", "rationale": "Culture and sensitivities", "urgency": "ROUTINE"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "UTI guidelines"
    },
    "Pyelonephritis": {
        "first_line": [
            {"test": "Urine MCS", "rationale": "Culture and sensitivities", "urgency": "URGENT"},
            {"test": "Ultrasound Renal Tract", "rationale": "Rule out obstruction", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Pyelonephritis guidelines"
    },
    "Cellulitis": {
        "first_line": [
            {"test": "Wound Swab", "rationale": "Culture if discharging", "urgency": "ROUTINE"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Cellulitis guidelines"
    },
    "Malaria": {
        "first_line": [
            {"test": "Thick and Thin Blood Films", "rationale": "Identify Plasmodium species", "urgency": "URGENT"},
            {"test": "Rapid Diagnostic Test (RDT)", "rationale": "Quick screening", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Malaria guidelines"
    },
    "Typhoid": {
        "first_line": [
            {"test": "Blood culture", "rationale": "Identify Salmonella Typhi", "urgency": "URGENT"},
            {"test": "Widal test", "rationale": "Serology (if culture unavailable)", "urgency": "ROUTINE"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Typhoid guidelines"
    },
    "Stroke (Ischaemic)": {
        "first_line": [
            {"test": "CT Head (non-contrast)", "rationale": "Rule out hemorrhage", "urgency": "EMERGENCY"},
            {"test": "CT Angiogram", "rationale": "For thrombectomy suitability", "urgency": "EMERGENCY"},
        ],
        "second_line": [
            {"test": "MRI Brain", "rationale": "More sensitive for infarction", "urgency": "URGENT"}
        ],
        "scoring_systems": ["NIHSS"],
        "guideline": "Stroke guidelines"
    },
    "Intracerebral Haemorrhage": {
        "first_line": [
            {"test": "CT Head (non-contrast)", "rationale": "Identify bleed", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["ICH Score"],
        "guideline": "Stroke guidelines"
    },
    "TIA": {
        "first_line": [
            {"test": "MRI Brain", "rationale": "DWI to check for small infarct", "urgency": "URGENT"},
            {"test": "Carotid Doppler", "rationale": "Check for stenosis", "urgency": "URGENT"},
            {"test": "ECG", "rationale": "Check for AF", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["ABCD2"],
        "guideline": "TIA guidelines"
    },
    "Status Epilepticus": {
        "first_line": [
            {"test": "Blood Glucose", "rationale": "Rule out hypoglycemia", "urgency": "EMERGENCY"},
            {"test": "EEG", "rationale": "Assess seizure activity", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Epilepsy guidelines"
    },
    "DVT": {
        "first_line": [
            {"test": "Doppler Ultrasound Leg", "rationale": "Identify clot", "urgency": "URGENT"},
            {"test": "D-dimer", "rationale": "Rule out if low risk", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": ["Wells Score for DVT"],
        "guideline": "DVT guidelines"
    },
    "Renal Colic": {
        "first_line": [
            {"test": "CT KUB", "rationale": "Identify calculus", "urgency": "URGENT"},
            {"test": "Urine Dipstick", "rationale": "Check for hematuria/infection", "urgency": "ROUTINE"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Renal Colic guidelines"
    },
    "Acute Urinary Retention": {
        "first_line": [
            {"test": "Bladder Scan", "rationale": "Measure retained volume", "urgency": "URGENT"},
            {"test": "U&E", "rationale": "Check for AKI", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "AUR guidelines"
    },
    "Ectopic Pregnancy": {
        "first_line": [
            {"test": "Serum bHCG", "rationale": "Confirm pregnancy", "urgency": "EMERGENCY"},
            {"test": "Transvaginal Ultrasound", "rationale": "Locate pregnancy", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Ectopic Pregnancy guidelines"
    },
    "Pre-eclampsia": {
        "first_line": [
            {"test": "Urine Protein/Creatinine Ratio", "rationale": "Quantify proteinuria", "urgency": "URGENT"},
            {"test": "U&E, LFT, FBC", "rationale": "Assess for HELLP syndrome", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Pre-eclampsia guidelines"
    },
    "Iron Deficiency Anaemia": {
        "first_line": [
            {"test": "Ferritin, Iron Studies", "rationale": "Confirm iron deficiency", "urgency": "ROUTINE"},
            {"test": "Coeliac Screen", "rationale": "Identify cause", "urgency": "ROUTINE"},
        ],
        "second_line": [
            {"test": "OGD/Colonoscopy", "rationale": "Rule out GI bleed/malignancy", "urgency": "ROUTINE"}
        ],
        "scoring_systems": [],
        "guideline": "IDA guidelines"
    },
    "B12 Deficiency": {
        "first_line": [
            {"test": "Serum B12", "rationale": "Confirm deficiency", "urgency": "ROUTINE"},
            {"test": "Intrinsic Factor Antibodies", "rationale": "Check for pernicious anemia", "urgency": "ROUTINE"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "B12 Deficiency guidelines"
    },
    "Thrombocytopenia": {
        "first_line": [
            {"test": "Blood Film", "rationale": "Check for clumping or hemolysis", "urgency": "URGENT"},
            {"test": "Coagulation Screen", "rationale": "Assess for DIC", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Thrombocytopenia guidelines"
    },
    "DIC": {
        "first_line": [
            {"test": "Fibrinogen", "rationale": "Decreased in consumption", "urgency": "EMERGENCY"},
            {"test": "D-dimer", "rationale": "Markedly elevated", "urgency": "EMERGENCY"},
            {"test": "PT/APTT", "rationale": "Prolonged", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["ISTH DIC Score"],
        "guideline": "DIC guidelines"
    },
    "Septic Arthritis": {
        "first_line": [
            {"test": "Joint Aspiration", "rationale": "Synovial fluid MCS and crystals", "urgency": "EMERGENCY"},
            {"test": "Blood cultures", "rationale": "Identify pathogen", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Septic Arthritis guidelines"
    },
    "Osteomyelitis": {
        "first_line": [
            {"test": "MRI of affected area", "rationale": "Most sensitive imaging", "urgency": "URGENT"},
            {"test": "Bone biopsy/culture", "rationale": "Identify pathogen", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Osteomyelitis guidelines"
    },
    "Gout": {
        "first_line": [
            {"test": "Joint Aspiration", "rationale": "Negatively birefringent urate crystals", "urgency": "URGENT"},
            {"test": "Serum Urate", "rationale": "Often normal during acute attack", "urgency": "ROUTINE"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Gout guidelines"
    },
    "Paracetamol Overdose": {
        "first_line": [
            {"test": "Paracetamol Level", "rationale": "Taken 4 hours post-ingestion", "urgency": "EMERGENCY"},
            {"test": "LFT, U&E, Coagulation", "rationale": "Assess for liver failure", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": ["King's College Criteria"],
        "guideline": "Toxbase"
    },
    "Opioid Overdose": {
        "first_line": [
            {"test": "ABG/VBG", "rationale": "Assess respiratory depression/acidosis", "urgency": "EMERGENCY"},
            {"test": "Paracetamol Level", "rationale": "Rule out co-ingestion", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Toxbase"
    },
    "CO Poisoning": {
        "first_line": [
            {"test": "Carboxyhemoglobin (ABG/VBG)", "rationale": "Confirm exposure level", "urgency": "EMERGENCY"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Toxbase"
    },
    "Anaphylaxis": {
        "first_line": [
            {"test": "Serum Tryptase", "rationale": "Taken shortly after, then at 1-2h and 24h", "urgency": "URGENT"},
        ],
        "second_line": [],
        "scoring_systems": [],
        "guideline": "Resuscitation Council UK Anaphylaxis"
    }
}

def recommend_investigations(
    differential_diagnoses: List[str],
    confidence: float,
    syndrome_name: Optional[str] = None
) -> Dict[str, Any]:
    """Returns prioritized investigation list for the top differential diagnoses."""
    recommendations = {}
    for diag in differential_diagnoses:
        if diag in INVESTIGATION_MAP:
            recommendations[diag] = INVESTIGATION_MAP[diag]
    return recommendations

def get_investigation_urgency(test: str) -> str:
    """Returns urgency: EMERGENCY / URGENT / ROUTINE / NON-URGENT"""
    test_lower = test.lower()
    for condition, data in INVESTIGATION_MAP.items():
        for item in data.get("first_line", []):
            if item["test"].lower() == test_lower:
                return item["urgency"]
        for item in data.get("second_line", []):
            if item["test"].lower() == test_lower:
                return item["urgency"]
    return "ROUTINE"
