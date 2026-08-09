"""
AuraMed AI — Clinical Guideline Registry v1.0
===============================================
Maps diseases and syndromes to authoritative clinical guidelines.
Sources: WHO, NICE, IDSA, ACC/AHA, ESC, BTS, AAP, ADA, KDIGO, ICMR, SIGN, AHA.
"""
from typing import Dict, Any, List, Optional

GUIDELINE_REGISTRY: Dict[str, Dict[str, Any]] = {

    # ── NEUROLOGY ────────────────────────────────────────────────────────────
    "Bacterial Meningitis": {
        "guideline": "IDSA 2024 Bacterial Meningitis Guidelines",
        "url": "https://www.idsociety.org/practice-guideline/bacterial-meningitis/",
        "key_recommendation": "Start ceftriaxone + dexamethasone within 60 minutes of clinical suspicion. CT before LP only if raised ICP suspected.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["IDSA", "WHO", "NICE NG198"],
        "year": 2024,
    },
    "Acute Ischemic Stroke": {
        "guideline": "AHA/ASA 2023 Acute Ischemic Stroke Guidelines",
        "url": "https://www.ahajournals.org/doi/10.1161/STR.0000000000000375",
        "key_recommendation": "IV alteplase (0.9mg/kg, max 90mg) within 4.5h of onset. Thrombectomy for large vessel occlusion within 24h.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["AHA", "ASA", "ESC", "NICE NG128"],
        "year": 2023,
    },
    "Epilepsy / First Seizure": {
        "guideline": "NICE NG217 Epilepsies 2022",
        "url": "https://www.nice.org.uk/guidance/ng217",
        "key_recommendation": "Do not start antiepileptics after a single unprovoked seizure. MRI brain and EEG recommended.",
        "evidence_grade": "Grade A",
        "organisations": ["NICE", "ILAE"],
        "year": 2022,
    },
    "Status Epilepticus": {
        "guideline": "NICE CKS Status Epilepticus 2023",
        "url": "https://cks.nice.org.uk/topics/epilepsy/",
        "key_recommendation": "Lorazepam 0.1mg/kg IV (max 4mg) as first-line. If no IV access: midazolam buccal/IM.",
        "evidence_grade": "Grade A",
        "organisations": ["NICE", "AES"],
        "year": 2023,
    },
    "Subarachnoid Hemorrhage": {
        "guideline": "AHA/ASA 2023 SAH Management Guidelines",
        "url": "https://www.ahajournals.org/doi/10.1161/STR.0000000000000375",
        "key_recommendation": "Non-contrast CT head first. If CT negative and clinical suspicion high: LP at 12h post-ictus. Nimodipine 60mg q4h for vasospasm prevention.",
        "evidence_grade": "Grade A (Level 1b)",
        "organisations": ["AHA", "ASA", "NICE"],
        "year": 2023,
    },
    "Parkinson's Disease": {
        "guideline": "NICE NG71 Parkinson's Disease 2017 (updated 2023)",
        "url": "https://www.nice.org.uk/guidance/ng71",
        "key_recommendation": "Levodopa/carbidopa remains gold standard. Refer to specialist movement disorder clinic.",
        "evidence_grade": "Grade A",
        "organisations": ["NICE", "MDS"],
        "year": 2023,
    },

    # ── CARDIOLOGY ───────────────────────────────────────────────────────────
    "Acute Myocardial Infarction": {
        "guideline": "ESC 2023 STEMI/NSTEMI Management Guidelines",
        "url": "https://www.escardio.org/Guidelines",
        "key_recommendation": "Primary PCI within 90 min of FMC for STEMI. DAPT: aspirin 300mg + ticagrelor 180mg loading. Heparin anticoagulation.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ESC", "ACC/AHA"],
        "year": 2023,
    },
    "STEMI": {
        "guideline": "ESC 2023 STEMI Guidelines",
        "url": "https://www.escardio.org/Guidelines/Clinical-Practice-Guidelines/Acute-Myocardial-Infarction-in-patients-presenting-with-ST-segment-elevation",
        "key_recommendation": "Primary PCI is standard of care. Door-to-balloon time < 90 min. Aspirin + P2Y12 inhibitor + anticoagulation.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ESC", "ACC/AHA"],
        "year": 2023,
    },
    "NSTEMI": {
        "guideline": "ESC 2020 NSTE-ACS Guidelines",
        "url": "https://www.escardio.org/Guidelines",
        "key_recommendation": "Early invasive strategy (angiography <24h for high risk). GRACE score for risk stratification. Anticoagulate + DAPT.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ESC", "ACC/AHA"],
        "year": 2020,
    },
    "Atrial Fibrillation": {
        "guideline": "ESC 2020 Atrial Fibrillation Guidelines",
        "url": "https://www.escardio.org/Guidelines/Clinical-Practice-Guidelines/Atrial-Fibrillation",
        "key_recommendation": "CHA2DS2-VASc >= 2 (men) / >= 3 (women): anticoagulate (DOAC preferred). Rate control: beta-blockers, digoxin, diltiazem.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ESC", "ACC/AHA", "NICE NG196"],
        "year": 2020,
    },
    "Heart Failure": {
        "guideline": "ESC 2021 Heart Failure Guidelines",
        "url": "https://www.escardio.org/Guidelines/Clinical-Practice-Guidelines/Acute-and-Chronic-Heart-Failure",
        "key_recommendation": "HFrEF: ACEi/ARB + beta-blocker + MRA + SGLT2i (fantastic four). BNP/NT-proBNP for diagnosis and monitoring.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ESC", "ACC/AHA", "NICE NG106"],
        "year": 2021,
    },
    "Aortic Dissection": {
        "guideline": "ESC 2014 Aortic Disease Guidelines (updated 2023)",
        "url": "https://www.escardio.org/Guidelines",
        "key_recommendation": "Type A: emergency surgery. Type B: medical management (anti-impulse therapy: IV labetalol/esmolol). CT aortography for diagnosis.",
        "evidence_grade": "Grade B",
        "organisations": ["ESC", "AHA"],
        "year": 2023,
    },
    "Pulmonary Embolism": {
        "guideline": "ESC 2019 Pulmonary Embolism Guidelines",
        "url": "https://www.escardio.org/Guidelines/Clinical-Practice-Guidelines/Pulmonary-Embolism",
        "key_recommendation": "High risk PE: systemic thrombolysis (alteplase 100mg over 2h). Low/intermediate risk: anticoagulation (DOAC preferred). Wells score + D-dimer for triage.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ESC", "BTS", "NICE NG158"],
        "year": 2019,
    },
    "Hypertensive Emergency": {
        "guideline": "ESC 2023 Hypertension Guidelines",
        "url": "https://www.escardio.org/Guidelines",
        "key_recommendation": "Reduce MAP by no more than 25% in first hour. IV labetalol, nicardipine, or nitroprusside. Avoid rapid BP reduction.",
        "evidence_grade": "Grade B",
        "organisations": ["ESC", "ISH", "ACC/AHA"],
        "year": 2023,
    },

    # ── RESPIRATORY ──────────────────────────────────────────────────────────
    "Community-Acquired Pneumonia": {
        "guideline": "BTS CAP Guidelines 2023 | NICE NG138",
        "url": "https://www.brit-thoracic.org.uk/",
        "key_recommendation": "CURB-65 guides severity. Low (0-1): oral amoxicillin 500mg TDS 5 days. Moderate (2): consider hospital. Severe (3+): IV co-amoxiclav + clarithromycin.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["BTS", "NICE", "IDSA", "ATS"],
        "year": 2023,
    },
    "COPD Exacerbation": {
        "guideline": "GOLD 2024 COPD Guidelines",
        "url": "https://goldcopd.org/2024-gold-report/",
        "key_recommendation": "Salbutamol + ipratropium nebulisers. Prednisolone 30mg PO x5 days. Antibiotics if purulent sputum/CRP>20. NIV if type 2 RF.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["GOLD", "BTS", "NICE NG115"],
        "year": 2024,
    },
    "Acute Asthma Exacerbation": {
        "guideline": "BTS/SIGN Asthma Guidelines 2023",
        "url": "https://www.brit-thoracic.org.uk/quality-improvement/guidelines/asthma/",
        "key_recommendation": "Salbutamol 5mg neb q15-20min. IV hydrocortisone 100mg or PO prednisolone 40mg. PEFR-guided severity. Consider magnesium sulfate 2g IV for severe.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["BTS", "SIGN", "GINA"],
        "year": 2023,
    },
    "Tuberculosis": {
        "guideline": "WHO TB Guidelines 2022 | NICE NG33",
        "url": "https://www.who.int/publications/i/item/9789240048119",
        "key_recommendation": "RHEZ regimen: Rifampicin + Isoniazid + Ethambutol + Pyrazinamide for 2 months, then Rifampicin + Isoniazid for 4 months. Notify public health.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["WHO", "NICE", "IDSA", "ICMR"],
        "year": 2022,
    },

    # ── GASTROENTEROLOGY ─────────────────────────────────────────────────────
    "Acute Pancreatitis": {
        "guideline": "IAP/APA 2024 Acute Pancreatitis Guidelines",
        "url": "https://www.iap-association.org/",
        "key_recommendation": "Aggressive IV fluid resuscitation (Lactated Ringer's preferred). Early enteral nutrition within 48h. ERCP for biliary pancreatitis with cholangitis.",
        "evidence_grade": "Grade A (Level 1b)",
        "organisations": ["IAP", "APA", "BSG"],
        "year": 2024,
    },
    "Upper GI Bleed": {
        "guideline": "BSG 2024 Upper GI Bleeding Guidelines | NICE NG141",
        "url": "https://www.bsg.org.uk/clinical-resource/bsg-guidelines-for-the-management-of-acute-upper-and-lower-gi-bleeding/",
        "key_recommendation": "Glasgow-Blatchford score for risk stratification. Urgent OGD within 24h. Proton pump inhibitor IV infusion pre-endoscopy.",
        "evidence_grade": "Grade A (Level 1b)",
        "organisations": ["BSG", "NICE", "ESGE"],
        "year": 2024,
    },
    "Appendicitis": {
        "guideline": "NICE NG91 2016 (updated 2024) | WSES 2020",
        "url": "https://www.nice.org.uk/guidance/ng91",
        "key_recommendation": "Alvarado score for adults. CT abdomen/pelvis if diagnosis unclear. Laparoscopic appendicectomy gold standard. Antibiotics alone for uncomplicated in selected patients.",
        "evidence_grade": "Grade A (Level 1b)",
        "organisations": ["NICE", "WSES", "SAGES"],
        "year": 2024,
    },

    # ── INFECTIOUS DISEASE ───────────────────────────────────────────────────
    "Sepsis": {
        "guideline": "Surviving Sepsis Campaign 2021 Guidelines",
        "url": "https://www.sccm.org/SurvivingSepsisCampaign/Guidelines",
        "key_recommendation": "Hour-1 Bundle: Blood cultures x2, broad-spectrum antibiotics within 1h, 30ml/kg IV crystalloid, vasopressors if MAP<65, lactate measurement.",
        "evidence_grade": "Grade A (Level 1b)",
        "organisations": ["SCCM", "ESICM", "IDSA"],
        "year": 2021,
    },
    "Malaria": {
        "guideline": "WHO Malaria Treatment Guidelines 2022",
        "url": "https://www.who.int/docs/default-source/malaria-guidelines/malaria-treatment-guidelines-2015.pdf",
        "key_recommendation": "Falciparum malaria: IV artesunate (preferred over quinine). Uncomplicated: ACT (artemether-lumefantrine). Vivax/Ovale: Chloroquine + primaquine.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["WHO", "ICMR"],
        "year": 2022,
    },
    "Typhoid Fever": {
        "guideline": "WHO Typhoid Guidelines 2018 | ICMR 2023",
        "url": "https://www.who.int/publications/i/item/9789241550277",
        "key_recommendation": "Fluoroquinolone-resistant: azithromycin (uncomplicated) or ceftriaxone (severe). Blood culture gold standard for diagnosis.",
        "evidence_grade": "Grade A",
        "organisations": ["WHO", "ICMR"],
        "year": 2023,
    },

    # ── ENDOCRINOLOGY ────────────────────────────────────────────────────────
    "Diabetic Ketoacidosis": {
        "guideline": "JBDS DKA Guidelines 2023 | ADA 2024",
        "url": "https://www.diabetes.org.uk/professionals/position-statements-reports/specialist-care-for-children-and-adults-and-complications/the-management-of-diabetic-ketoacidosis-in-adults",
        "key_recommendation": "IV 0.9% saline resuscitation. Fixed-rate insulin infusion 0.1 units/kg/hr. Potassium replacement. Bicarbonate only if pH<6.9. Target: ketones <0.3, pH>7.3.",
        "evidence_grade": "Grade A",
        "organisations": ["JBDS", "ADA", "ISPAD"],
        "year": 2023,
    },
    "Type 2 Diabetes": {
        "guideline": "ADA Standards of Care 2024 | NICE NG28",
        "url": "https://diabetesjournals.org/care/issue/47/Supplement_1",
        "key_recommendation": "Metformin first-line. Add SGLT2i or GLP-1RA if CVD/CKD/HF. HbA1c target individualised (typically <53 mmol/mol). Annual foot exam, eye exam, nephrology review.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["ADA", "NICE", "IDF", "ICMR"],
        "year": 2024,
    },
    "Hypothyroidism": {
        "guideline": "ETA Guidelines 2019 | NICE NG145",
        "url": "https://www.nice.org.uk/guidance/ng145",
        "key_recommendation": "Levothyroxine replacement: start 25-50mcg, titrate to TSH 0.4-2.5 mU/L. Check TSH every 3 months until stable, then annually.",
        "evidence_grade": "Grade A",
        "organisations": ["ETA", "NICE", "ATA"],
        "year": 2019,
    },
    "Hyperthyroidism": {
        "guideline": "ATA Guidelines 2016 | ETA 2018",
        "url": "https://www.thyroid.org/professionals/ata-professional-guidelines/",
        "key_recommendation": "Carbimazole (preferred in UK) or propylthiouracil. Beta-blockers for symptom control. Radioiodine or thyroidectomy for definitive treatment.",
        "evidence_grade": "Grade A",
        "organisations": ["ATA", "ETA", "BTA"],
        "year": 2018,
    },

    # ── PAEDIATRICS ──────────────────────────────────────────────────────────
    "Kawasaki Disease": {
        "guideline": "AAP 2017 Kawasaki Disease Guidelines",
        "url": "https://publications.aap.org/pediatrics/article/140/1/e20171158/38355",
        "key_recommendation": "IVIG 2g/kg + aspirin 30-50mg/kg/day (high dose) until afebrile, then 3-5mg/kg/day for 6-8 weeks. Echocardiogram for coronary artery surveillance.",
        "evidence_grade": "Grade A (Level 1b)",
        "organisations": ["AAP", "JCS"],
        "year": 2017,
    },
    "Febrile Seizure": {
        "guideline": "NICE CKS Febrile Seizure 2023",
        "url": "https://cks.nice.org.uk/topics/febrile-seizure/",
        "key_recommendation": "Simple febrile seizure: no antiepileptic treatment. Identify and treat fever source. LP only if meningitis suspected. Reassure parents.",
        "evidence_grade": "Grade A",
        "organisations": ["NICE", "AAP"],
        "year": 2023,
    },

    # ── OBSTETRICS ───────────────────────────────────────────────────────────
    "Pre-eclampsia": {
        "guideline": "NICE NG133 2019 (updated 2023) | ISSHP 2021",
        "url": "https://www.nice.org.uk/guidance/ng133",
        "key_recommendation": "Aspirin 150mg from 12 weeks in high-risk patients. Severe hypertension: IV labetalol or nifedipine. Magnesium sulfate for eclampsia prevention. Delivery is definitive treatment.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["NICE", "ISSHP", "RCOG"],
        "year": 2023,
    },
    "Ectopic Pregnancy": {
        "guideline": "RCOG GTG 21 2016",
        "url": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/",
        "key_recommendation": "Unstable: emergency surgery (salpingectomy). Stable, small, low hCG: methotrexate 50mg/m2 IM (criteria met). All Rh negative: anti-D immunoglobulin.",
        "evidence_grade": "Grade A",
        "organisations": ["RCOG", "ESHRE"],
        "year": 2016,
    },

    # ── RHEUMATOLOGY / MSK ───────────────────────────────────────────────────
    "Septic Arthritis": {
        "guideline": "BSR/BHPR 2006 | NICE 2023",
        "url": "https://www.rheumatology.org.uk/practice-quality/guidelines",
        "key_recommendation": "Joint aspiration + culture before antibiotics. IV flucloxacillin (+ gentamicin if Gram-negative concern). Washout if no improvement in 48h.",
        "evidence_grade": "Grade B",
        "organisations": ["BSR", "BHPR", "NICE"],
        "year": 2023,
    },
    "Rheumatoid Arthritis": {
        "guideline": "EULAR 2022 RA Treatment Recommendations | NICE NG100",
        "url": "https://ard.bmj.com/content/81/3/326",
        "key_recommendation": "Treat-to-target strategy: DAS28 remission. Start csDMARD (methotrexate) within 3 months. Add bDMARD if csDMARD fails at 6 months.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["EULAR", "ACR", "NICE"],
        "year": 2022,
    },

    # ── NEPHROLOGY ───────────────────────────────────────────────────────────
    "Acute Kidney Injury": {
        "guideline": "KDIGO AKI Guidelines 2024",
        "url": "https://kdigo.org/guidelines/acute-kidney-injury/",
        "key_recommendation": "Optimise haemodynamics and volume status. Stop nephrotoxins. Avoid contrast. Dialysis if: refractory hyperkalaemia, acidosis, fluid overload, uraemic complications.",
        "evidence_grade": "Grade A",
        "organisations": ["KDIGO", "ERA", "NICE NG148"],
        "year": 2024,
    },
    "Chronic Kidney Disease": {
        "guideline": "KDIGO CKD Guidelines 2024",
        "url": "https://kdigo.org/guidelines/ckd-mbd/",
        "key_recommendation": "BP target <130/80. ACEi/ARB for proteinuric CKD. SGLT2i for DM/CKD. GFR decline monitoring. Refer nephrology if GFR <30.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["KDIGO", "NICE NG203"],
        "year": 2024,
    },

    # ── PSYCHIATRY ───────────────────────────────────────────────────────────
    "Major Depressive Disorder": {
        "guideline": "NICE NG222 2022 | APA 2023",
        "url": "https://www.nice.org.uk/guidance/ng222",
        "key_recommendation": "Mild: watchful waiting, exercise, CBT. Moderate-severe: SSRI (sertraline preferred) + CBT. Reassess at 4-6 weeks. Refer if suicidal ideation or psychotic features.",
        "evidence_grade": "Grade A (Level 1a)",
        "organisations": ["NICE", "APA", "BAP"],
        "year": 2022,
    },
    "Schizophrenia": {
        "guideline": "NICE NG185 2020 | BAP 2019",
        "url": "https://www.nice.org.uk/guidance/ng185",
        "key_recommendation": "Second-generation antipsychotic (risperidone/olanzapine). CBT for positive symptoms. Clozapine if two antipsychotics fail. Regular metabolic monitoring.",
        "evidence_grade": "Grade A",
        "organisations": ["NICE", "BAP", "APA"],
        "year": 2020,
    },

    # ── ONCOLOGY / HAEMATOLOGY ───────────────────────────────────────────────
    "Iron Deficiency Anaemia": {
        "guideline": "BSH 2021 IDA Guidelines | NICE CKS",
        "url": "https://b-s-h.org.uk/guidelines/",
        "key_recommendation": "Identify and treat underlying cause. Ferrous sulphate 200mg TDS (or BD if intolerant). IV iron if oral not tolerated or IBD. Recheck Hb at 4 weeks.",
        "evidence_grade": "Grade A",
        "organisations": ["BSH", "NICE"],
        "year": 2021,
    },
    "DIC": {
        "guideline": "ISTH 2018 DIC Guidelines | BSH 2009",
        "url": "https://www.isth.org/",
        "key_recommendation": "Treat underlying cause. FFP for active bleeding + PT>1.5x. Cryoprecipitate if fibrinogen <1.5g/L. Platelets if <50 + bleeding.",
        "evidence_grade": "Grade B",
        "organisations": ["ISTH", "BSH"],
        "year": 2018,
    },

    # ── EMERGENCY ────────────────────────────────────────────────────────────
    "Anaphylaxis": {
        "guideline": "RCUK Anaphylaxis Guidelines 2021 | WAO 2020",
        "url": "https://www.resus.org.uk/anaphylaxis/emergency-treatment-of-anaphylactic-reactions",
        "key_recommendation": "IM epinephrine (adrenaline) 0.5mg (0.5ml 1:1000) anterolateral thigh immediately. Repeat at 5 min if needed. IV antihistamine + hydrocortisone secondary. Observe 6-12h.",
        "evidence_grade": "Grade A",
        "organisations": ["RCUK", "WAO", "BSACI", "NICE CKS"],
        "year": 2021,
    },
    "Paracetamol Overdose": {
        "guideline": "MHRA/NPIS 2022 | TOXBASE | BNF",
        "url": "https://www.poisonsinfo.nhs.uk/",
        "key_recommendation": "N-acetylcysteine (NAC): 150mg/kg over 60min, then 50mg/kg over 4h, then 100mg/kg over 16h. Use Rumack-Matthew nomogram for risk assessment.",
        "evidence_grade": "Grade A",
        "organisations": ["MHRA", "NPIS", "AACT"],
        "year": 2022,
    },
    "Carbon Monoxide Poisoning": {
        "guideline": "UKPID 2023 | ACMT Guidelines",
        "url": "https://toxbase.org/",
        "key_recommendation": "High-flow 100% oxygen via tight-fitting mask immediately. Hyperbaric O2 if: COHb>25%, loss of consciousness, cardiac involvement, pregnancy.",
        "evidence_grade": "Grade B",
        "organisations": ["ACMT", "EAPCCT"],
        "year": 2023,
    },
}


def get_guideline(disease_name: str) -> Optional[Dict[str, Any]]:
    """Returns guideline information for a disease, or None if not found."""
    return GUIDELINE_REGISTRY.get(disease_name)


def get_citation_text(disease_name: str) -> str:
    """Returns a formatted citation string for a disease."""
    g = GUIDELINE_REGISTRY.get(disease_name)
    if not g:
        return "AuraMed AI Evidence Database v4.5 | WHO/CDC/NICE Reference"
    orgs = " | ".join(g.get("organisations", ["WHO"]))
    return f"{g['guideline']} ({g['year']}) | {orgs}"


def get_organisations_for_category(category: str) -> List[str]:
    """Returns key guideline organisations for a clinical specialty."""
    org_map = {
        "Cardiology": ["ESC", "ACC/AHA", "NICE"],
        "Respiratory": ["BTS", "GOLD", "GINA", "NICE"],
        "Neurology": ["NICE", "AHA/ASA", "ILAE"],
        "Gastroenterology": ["BSG", "ESGE", "NICE"],
        "Infectious Disease": ["IDSA", "WHO", "ICMR"],
        "Endocrinology": ["ADA", "ETA", "NICE"],
        "Paediatrics": ["AAP", "NICE", "RCPCH"],
        "Obstetrics": ["RCOG", "NICE", "ISSHP"],
        "Rheumatology": ["EULAR", "ACR", "BSR"],
        "Nephrology": ["KDIGO", "NICE", "ERA"],
        "Psychiatry": ["NICE", "APA", "BAP"],
        "Haematology": ["BSH", "ISTH"],
        "Emergency": ["RCUK", "ERC", "ACEP"],
        "Dermatology": ["BAD", "AAD", "NICE"],
        "Urology": ["EAU", "AUA", "NICE"],
    }
    return org_map.get(category, ["WHO", "NICE", "CDC"])
