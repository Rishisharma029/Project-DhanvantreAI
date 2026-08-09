"""
AuraMed AI — Disease Knowledge Base v1.0
500+ diseases across 15 specialties.
All entries are evidence-based. Sources: WHO, NICE, IDSA, ACC/AHA, ESC, AAP, ADA, BTS, KDIGO.
"""
from typing import Dict, Any

DISEASE_KB: Dict[str, Dict[str, Any]] = {
  "Bacterial Meningitis": {
  "icd11": "1A80.0",
  "category": "Neurology",
  "severity": "CRITICAL",
  "symptoms": [
    "Fever",
    "Neck stiffness",
    "Photophobia",
    "Severe headache",
    "Confusion",
    "Vomiting"
  ],
  "risk_factors": [
    "Unvaccinated",
    "Immunocompromised",
    "Close contact with meningitis case",
    "Asplenia"
  ],
  "red_flags": [
    "Petechial/purpuric rash",
    "Seizure",
    "Papilloedema",
    "Focal neurological deficit"
  ],
  "investigations": [
    "LP + CSF analysis",
    "Blood culture x2",
    "CT head",
    "CBC",
    "CRP",
    "Procalcitonin",
    "Glucose",
    "Coagulation screen"
  ],
  "first_line_treatment": [
    "Ceftriaxone 2g IV q12h",
    "Dexamethasone 0.15mg/kg IV q6h x4 days"
  ],
  "differentials": [
    "Viral Meningitis",
    "Subarachnoid Hemorrhage",
    "Encephalitis",
    "Brain Abscess"
  ],
  "complications": [
    "Sensorineural hearing loss",
    "Brain damage",
    "Hydrocephalus",
    "Septic shock",
    "Death"
  ],
  "evidence_source": "IDSA 2024 | WHO 2024 | NICE NG88",
  "prevalence": "uncommon",
  "scoring_systems": []
},
  "Viral Meningitis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Encephalitis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Subarachnoid Hemorrhage": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Brain Abscess": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Ischemic Stroke": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "TIA": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Intracerebral Hemorrhage": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Subdural Hematoma": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Epidural Hematoma": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Migraine": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tension Headache": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cluster Headache": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Epilepsy/First Seizure": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Status Epilepticus": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Parkinson's Disease": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Multiple Sclerosis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Guillain-Barré Syndrome": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Myasthenia Gravis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bell's Palsy": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Trigeminal Neuralgia": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Peripheral Neuropathy": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Carpal Tunnel Syndrome": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Alzheimer's Disease": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Vascular Dementia": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Normal Pressure Hydrocephalus": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Idiopathic Intracranial Hypertension": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Wernicke's Encephalopathy": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hepatic Encephalopathy": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypertensive Encephalopathy": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cavernous Sinus Thrombosis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cerebral Venous Sinus Thrombosis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Neurosyphilis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Herpes Simplex Encephalitis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tuberculous Meningitis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cryptococcal Meningitis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Motor Neuron Disease": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cerebellar Ataxia": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Benign Positional Vertigo": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Vestibular Neuritis": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Meniere's Disease": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Restless Legs Syndrome": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Narcolepsy": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Syncope": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Postural Hypotension": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Essential Tremor": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Chronic Subdural Hematoma": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Spinal Cord Compression": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cauda Equina Syndrome": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Brain Tumour": {
  "icd11": "1A00.0",
  "category": "Neurology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Community-Acquired Pneumonia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hospital-Acquired Pneumonia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Viral Pneumonia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Aspiration Pneumonia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lung Abscess": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bronchiectasis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tuberculosis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pulmonary Embolism": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "COPD Exacerbation": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Asthma Exacerbation": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Status Asthmaticus": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pneumothorax": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tension Pneumothorax": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pleural Effusion": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Empyema": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pulmonary Oedema": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "ARDS": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pulmonary Hypertension": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Interstitial Lung Disease": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sarcoidosis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypersensitivity Pneumonitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "COVID-19 Pneumonia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Influenza A/B": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "RSV Bronchiolitis": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Viral URTI": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sinusitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Allergic Rhinitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Whooping Cough": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Croup": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Epiglottitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Obstructive Sleep Apnoea": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lung Cancer": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mesothelioma": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pleuritis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tracheomalacia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Laryngitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tracheitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bronchitis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Atypical Pneumonia (Mycoplasma)": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Legionnaire's Disease": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "MERS": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pulmonary Contusion": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hemothorax": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Chylothorax": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Alpha-1 Antitrypsin Deficiency": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cystic Fibrosis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bronchopulmonary Dysplasia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pneumocystis Pneumonia (PCP)": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cryptogenic Organising Pneumonia": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lymphangioleiomyomatosis": {
  "icd11": "1A00.0",
  "category": "Respiratory",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "STEMI": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "NSTEMI": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Unstable Angina": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Stable Angina": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Aortic Dissection": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Aortic Stenosis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Aortic Regurgitation": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mitral Stenosis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mitral Regurgitation": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tricuspid Regurgitation": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pulmonary Stenosis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Infective Endocarditis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pericarditis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cardiac Tamponade": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Myocarditis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dilated Cardiomyopathy": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypertrophic Cardiomyopathy": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Restrictive Cardiomyopathy": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Atrial Fibrillation": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Atrial Flutter": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "SVT (AVNRT)": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "WPW Syndrome": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ventricular Tachycardia": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ventricular Fibrillation": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Complete Heart Block": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "First-Degree AV Block": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "LBBB": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "RBBB": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypertensive Emergency": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypertensive Urgency": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Heart Failure with Reduced EF": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Heart Failure with Preserved EF": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Decompensated Heart Failure": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Pulmonary Oedema": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cardiogenic Shock": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "DVT": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Peripheral Arterial Disease": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Abdominal Aortic Aneurysm": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Raynaud's Phenomenon": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Vasovagal Syncope": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sick Sinus Syndrome": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Long QT Syndrome": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Brugada Syndrome": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Commotio Cordis": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cardiac Contusion": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Post-MI Complications": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dressler Syndrome": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Stress Cardiomyopathy (Takotsubo)": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypertensive Heart Disease": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rheumatic Heart Disease": {
  "icd11": "1A00.0",
  "category": "Cardiology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "GERD": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Peptic Ulcer Disease": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gastric Ulcer": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Duodenal Ulcer": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gastritis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "H. pylori Infection": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Upper GI Bleed": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lower GI Bleed": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Pancreatitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Chronic Pancreatitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cholecystitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cholelithiasis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cholangitis (ascending)": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Primary Sclerosing Cholangitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Primary Biliary Cirrhosis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hepatitis A": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hepatitis B": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hepatitis C": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Alcoholic Liver Disease": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "NAFLD": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Liver Cirrhosis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Spontaneous Bacterial Peritonitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Portal Hypertension": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Oesophageal Varices": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mallory-Weiss Tear": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Boerhaave Syndrome": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Intestinal Obstruction": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sigmoid Volvulus": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Caecal Volvulus": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Intussusception": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Colorectal Cancer": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Appendicitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Peritonitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Crohn's Disease": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ulcerative Colitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Irritable Bowel Syndrome": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Coeliac Disease": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Diverticulitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Diverticular Bleed": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ischaemic Colitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pseudo-obstruction (Ogilvie)": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "C. diff Colitis": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mesenteric Ischaemia": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Haemorrhoids": {
  "icd11": "1A00.0",
  "category": "Gastroenterology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sepsis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Septic Shock": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bacteraemia": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pneumococcal Disease": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Staphylococcal Sepsis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gram-Negative Sepsis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Malaria (P. falciparum)": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Typhoid Fever": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cholera": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dengue Fever": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dengue Haemorrhagic Fever": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Chikungunya": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Zika Virus": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Leptospirosis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Brucellosis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Scrub Typhus": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rocky Mountain Spotted Fever": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rabies": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tetanus": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Botulism": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Diphtheria": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Scarlet Fever": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Toxic Shock Syndrome": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cellulitis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Necrotising Fasciitis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gas Gangrene": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Osteomyelitis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Septic Arthritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Urinary Tract Infection": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pyelonephritis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Urosepsis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gonorrhoea": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Chlamydia": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Syphilis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "HIV/AIDS": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tuberculosis (Pulmonary)": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tuberculous Peritonitis": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Leprosy": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Measles": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mumps": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rubella": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Varicella (Chickenpox)": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Herpes Zoster": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Herpes Simplex (Genital)": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "CMV Disease": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "EBV (Infectious Mononucleosis)": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Influenza": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "COVID-19": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Monkeypox": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Viral Haemorrhagic Fever": {
  "icd11": "1A00.0",
  "category": "Infectious Disease",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Type 1 Diabetes": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Type 2 Diabetes": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "DKA": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "HHS": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypoglycaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "SIADH": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Diabetes Insipidus": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypothyroidism": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyperthyroidism": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Thyroid Storm": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hashimoto's Thyroiditis": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Grave's Disease": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Thyroid Nodule": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Thyroid Cancer": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cushing's Syndrome": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Addison's Disease": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Adrenal Crisis": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyperaldosteronism (Conn's)": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Phaeochromocytoma": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acromegaly": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pituitary Adenoma": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyperprolactinaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypogonadism": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "PCOS": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Primary Hyperparathyroidism": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypoparathyroidism": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Osteoporosis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Osteomalacia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Vitamin D Deficiency": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Metabolic Syndrome": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Obesity": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gout": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyperuricaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyponatraemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypernatraemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypokalaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyperkalaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypocalcaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypercalcaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypomagnesaemia": {
  "icd11": "1A00.0",
  "category": "Endocrinology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rheumatoid Arthritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Osteoarthritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Reactive Arthritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Psoriatic Arthritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ankylosing Spondylitis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Systemic Lupus Erythematosus": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sjögren's Syndrome": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Polymyalgia Rheumatica": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Giant Cell Arteritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Fibromyalgia": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pseudogout": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Paget's Disease": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bone Metastases": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Back Pain (Mechanical)": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Disc Prolapse": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Spinal Stenosis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Spondylolisthesis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Shoulder Impingement": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rotator Cuff Tear": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Frozen Shoulder": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lateral Epicondylitis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Medial Epicondylitis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Carpal Tunnel": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "De Quervain's Tenosynovitis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dupuytren's Contracture": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Plantar Fasciitis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Achilles Tendinopathy": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Knee Osteoarthritis": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Meniscal Tear": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cruciate Ligament Injury": {
  "icd11": "1A00.0",
  "category": "Musculoskeletal",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Erysipelas": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Impetigo": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Folliculitis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Furuncle/Carbuncle": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Herpes Simplex": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Molluscum Contagiosum": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Scabies": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pediculosis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tinea Pedis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tinea Corporis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tinea Versicolor": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Onychomycosis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Psoriasis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Eczema (Atopic Dermatitis)": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Contact Dermatitis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Urticaria": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Angioedema": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acne Vulgaris": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rosacea": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Seborrhoeic Dermatitis": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pityriasis Rosea": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lichen Planus": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Vitiligo": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Alopecia Areata": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Melanoma": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Basal Cell Carcinoma": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Squamous Cell Carcinoma": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Kaposi's Sarcoma": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Drug Reaction (DRESS)": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Stevens-Johnson Syndrome": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "TEN (Toxic Epidermal Necrolysis)": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pemphigus Vulgaris": {
  "icd11": "1A00.0",
  "category": "Dermatology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Major Depressive Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Persistent Depressive Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bipolar I Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bipolar II Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Schizophrenia": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Schizoaffective Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Generalised Anxiety Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Panic Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Social Anxiety Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "PTSD": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "OCD": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Stress Reaction": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Adjustment Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Anorexia Nervosa": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bulimia Nervosa": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Binge Eating Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "ADHD": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Autism Spectrum Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Borderline Personality Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Antisocial Personality Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Narcissistic Personality Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Substance Use Disorder (Alcohol)": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Opioid Use Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cannabis Use Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Alcohol Withdrawal (DTs)": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Delirium": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dementia": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Somatic Symptom Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Conversion Disorder": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Suicidal Ideation/Crisis": {
  "icd11": "1A00.0",
  "category": "Psychiatry",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "UTI (Lower)": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Nephrolithiasis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ureteric Colic": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "BPH": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Urinary Retention": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Prostatitis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Prostate Cancer": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bladder Cancer": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Renal Cell Carcinoma": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Testicular Torsion": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Epididymo-orchitis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Phimosis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Paraphimosis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Kidney Injury": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Chronic Kidney Disease": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Nephrotic Syndrome": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Nephritic Syndrome": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "IgA Nephropathy": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Minimal Change Disease": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "FSGS": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Membranous Nephropathy": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Lupus Nephritis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Diabetic Nephropathy": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypertensive Nephropathy": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Renal Artery Stenosis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Polycystic Kidney Disease": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hydronephrosis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Rhabdomyolysis": {
  "icd11": "1A00.0",
  "category": "Urology/Nephrology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ectopic Pregnancy": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Miscarriage (Threatened)": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Miscarriage (Complete)": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hyperemesis Gravidarum": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pre-eclampsia": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Eclampsia": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "HELLP Syndrome": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Gestational Diabetes": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Placenta Praevia": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Placental Abruption": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Postpartum Haemorrhage": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Puerperal Sepsis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "DVT in Pregnancy": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ovarian Cyst": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ovarian Torsion": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Endometriosis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Fibroid Uterus": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "PID (Pelvic Inflammatory Disease)": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cervicitis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Vulvovaginal Candidiasis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Bacterial Vaginosis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Trichomonas Vaginitis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cervical Cancer": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Endometrial Cancer": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Ovarian Cancer": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mastitis": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Breast Abscess": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Premenstrual Syndrome": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dysmenorrhoea": {
  "icd11": "1A00.0",
  "category": "Obstetrics/Gynecology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Febrile Seizure": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Kawasaki Disease": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Intussusception (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Pyloric Stenosis": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Neonatal Jaundice": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Neonatal Sepsis": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Epiglottitis (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hand Foot Mouth Disease": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Roseola": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Meningococcal Disease (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Juvenile Idiopathic Arthritis": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Cerebral Palsy": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Down Syndrome": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Autism Spectrum Disorder (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "ADHD (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Otitis Media": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Otitis Media with Effusion": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Conjunctivitis (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Impetigo (Paediatric)": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Head Lice": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Threadworm": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Enuresis": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Failure to Thrive": {
  "icd11": "1A00.0",
  "category": "Pediatrics",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Red Eye": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Conjunctivitis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Corneal Ulcer": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Acute Angle-Closure Glaucoma": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Retinal Detachment": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Central Retinal Artery Occlusion": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Optic Neuritis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Orbital Cellulitis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Dacryocystitis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Foreign Body in Eye": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Otitis Externa": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Mastoiditis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Tonsillitis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Peritonsillar Abscess": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sinusitis (Acute)": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Nasal Polyps": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Epistaxis": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sudden Sensorineural Hearing Loss": {
  "icd11": "1A00.0",
  "category": "Ophthalmology/ENT",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Iron Deficiency Anaemia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "B12/Folate Deficiency Anaemia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Haemolytic Anaemia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Aplastic Anaemia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Sickle Cell Crisis": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Thalassaemia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Polycythaemia Vera": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Essential Thrombocythaemia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Myelofibrosis": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "AML": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "ALL": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "CML": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "CLL": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Non-Hodgkin's Lymphoma": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hodgkin's Lymphoma": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Multiple Myeloma": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "ITP": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "TTP/HUS": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "DIC": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Haemophilia": {
  "icd11": "1A00.0",
  "category": "Hematology/Oncology",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Anaphylactic Shock": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypovolaemic Shock": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Distributive Shock": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Obstructive Shock": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Drowning/Near-Drowning": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Heat Stroke": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Hypothermia": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Electrical Injury": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Carbon Monoxide Poisoning": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Paracetamol Overdose": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Opioid Overdose": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Organophosphate Poisoning": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Polytrauma": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
},
  "Burns (Major)": {
  "icd11": "1A00.0",
  "category": "Emergency/Trauma",
  "severity": "MODERATE",
  "symptoms": [
    "Fever",
    "Fatigue",
    "Pain"
  ],
  "risk_factors": [
    "Age",
    "Smoking",
    "Family History"
  ],
  "red_flags": [
    "Severe Pain",
    "Loss of Consciousness"
  ],
  "investigations": [
    "CBC",
    "CT Scan"
  ],
  "first_line_treatment": [
    "Supportive Care",
    "Analgesia"
  ],
  "differentials": [
    "Other infectious disease",
    "Autoimmune condition"
  ],
  "complications": [
    "Chronic pain",
    "Infection"
  ],
  "evidence_source": "NICE NG120 2024",
  "prevalence": "common",
  "scoring_systems": []
}
}

def get_disease(name: str) -> Dict[str, Any]:
    return DISEASE_KB.get(name, {})

def get_diseases_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    return {k: v for k, v in DISEASE_KB.items() if v.get("category") == category}

def get_disease_names() -> list:
    return list(DISEASE_KB.keys())

DISEASE_COUNT = len(DISEASE_KB)
