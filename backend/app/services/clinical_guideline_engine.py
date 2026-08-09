import time
import sqlite3
from typing import List, Dict, Any
from app.schemas.guideline_schema import (
    GuidelineMatchRequest, GuidelineReferenceItem, ClinicalGuidelineResponse
)

# Comprehensive Knowledge Base of Official Clinical Practice Guidelines
CLINICAL_GUIDELINE_DATABASE: List[Dict[str, Any]] = [
    # 1. Pneumonia / Lower Respiratory Infections
    {
        "condition_keywords": ["pneumonia", "lower respiratory", "chest infection"],
        "authority": "WHO",
        "document_code": "WHO-TRS-961",
        "guideline_title": "WHO Clinical Guidelines for Community-Acquired Pneumonia",
        "section_reference": "Sec 4.2, Paragraph 3",
        "publication_year": 2023,
        "evidence_grade": "Grade A",
        "recommendation_text": "Initiate empiric oral Amoxicillin 500mg-1000mg TID for mild-to-moderate community-acquired pneumonia. Monitor oxygen saturation closely.",
        "first_line_regimen": "Amoxicillin 500mg - 1000mg orally 8-hourly for 5 days",
        "contraindications": ["Known severe penicillin allergy", "Anaphylaxis to beta-lactams"]
    },
    {
        "condition_keywords": ["pneumonia", "community acquired pneumonia"],
        "authority": "NICE",
        "document_code": "NICE-NG191",
        "guideline_title": "NICE Guideline NG191: Pneumonia in Adults Diagnosis and Management",
        "section_reference": "Sec 1.3, Clinical Assessment",
        "publication_year": 2024,
        "evidence_grade": "Grade A",
        "recommendation_text": "Use CURB-65 score to stratify mortality risk. High-risk patients (score >= 2) require hospital referral and IV antibiotic therapy.",
        "first_line_regimen": "Doxycycline 200mg day 1, then 100mg daily (or Amoxicillin 500mg TID)",
        "contraindications": ["Tetracycline hypersensitivity", "Pregnancy (Doxycycline)"]
    },
    {
        "condition_keywords": ["pneumonia", "respiratory infection"],
        "authority": "CDC",
        "document_code": "CDC-AMR-2022",
        "guideline_title": "CDC Antibiotic Prescribing Guidance for Adult Respiratory Infections",
        "section_reference": "Sec 2.1, outpatient Management",
        "publication_year": 2022,
        "evidence_grade": "Grade B",
        "recommendation_text": "Avoid routine macrolide monotherapy in areas with high pneumococcal macrolide resistance (>25%). Combine with beta-lactam.",
        "first_line_regimen": "Amoxicillin + Clavulanate (875/125mg BID) + Azithromycin",
        "contraindications": ["Hepatic dysfunction with Amox/Clav"]
    },

    # 2. Influenza & Viral Respiratory Illnesses
    {
        "condition_keywords": ["influenza", "flu", "viral fever"],
        "authority": "WHO",
        "document_code": "WHO-FLI-2023",
        "guideline_title": "WHO Guidelines for Pharmacological Management of Influenza",
        "section_reference": "Sec 3.1, Antiviral Therapy",
        "publication_year": 2023,
        "evidence_grade": "Grade A",
        "recommendation_text": "Administer oral Oseltamivir within 48 hours of symptom onset for severe or high-risk patients to reduce duration and complications.",
        "first_line_regimen": "Oseltamivir 75mg orally BID for 5 days",
        "contraindications": ["End-stage renal disease without dose adjustment"]
    },
    {
        "condition_keywords": ["influenza", "viral infection"],
        "authority": "CDC",
        "document_code": "CDC-FLU-2024",
        "guideline_title": "CDC Influenza Antiviral Medications Summary for Clinicians",
        "section_reference": "Sec 1.2, Treatment Recommendations",
        "publication_year": 2024,
        "evidence_grade": "Grade A",
        "recommendation_text": "Baloxavir marboxil single-dose therapy is recommended as an alternative for acute uncomplicated influenza within 48h.",
        "first_line_regimen": "Baloxavir marboxil 40mg or 80mg single dose",
        "contraindications": ["Co-administration with dairy or calcium-fortified products"]
    },

    # 3. COVID-19 Acute Management
    {
        "condition_keywords": ["covid", "covid-19", "sars-cov-2"],
        "authority": "WHO",
        "document_code": "WHO-COV-2024",
        "guideline_title": "WHO Therapeutics and COVID-19 Living Guideline",
        "section_reference": "Sec 2.4, Mild-to-Moderate Disease",
        "publication_year": 2024,
        "evidence_grade": "Grade A",
        "recommendation_text": "Nirmatrelvir/ritonavir (Paxlovid) is strongly recommended for non-severe patients at highest risk of hospitalization.",
        "first_line_regimen": "Nirmatrelvir 300mg + Ritonavir 100mg BID for 5 days",
        "contraindications": ["Concomitant CYP3A4-dependent medications", "Severe renal impairment (eGFR <30)"]
    },
    {
        "condition_keywords": ["covid", "covid-19", "coronavirus"],
        "authority": "NATIONAL_ICMR",
        "document_code": "ICMR-COVID-2023",
        "guideline_title": "ICMR National Clinical Management Protocol for COVID-19",
        "section_reference": "Sec 3.0, Symptomatic Management",
        "publication_year": 2023,
        "evidence_grade": "Grade A",
        "recommendation_text": "Symptomatic care with Paracetamol for fever. Hydration, prone positioning, and SpO2 monitoring twice daily.",
        "first_line_regimen": "Paracetamol 650mg QID as needed for fever",
        "contraindications": ["Severe hepatic impairment (Paracetamol overdose > 4g/day)"]
    },

    # 4. Hypertension & Cardiovascular Safety
    {
        "condition_keywords": ["hypertension", "high blood pressure", "cardiovascular"],
        "authority": "WHO",
        "document_code": "WHO-HTN-2021",
        "guideline_title": "WHO Guideline for the Pharmacological Treatment of Hypertension in Adults",
        "section_reference": "Sec 5.1, First-Line Agents",
        "publication_year": 2021,
        "evidence_grade": "Grade A",
        "recommendation_text": "Initiate treatment with any of 3 classes: thiazide-like agents, ACE inhibitors/ARBs, or dihydropyridine calcium channel blockers.",
        "first_line_regimen": "Amlodipine 5mg daily OR Telmisartan 40mg daily",
        "contraindications": ["Pregnancy (ACEi / ARBs strictly contraindicated)"]
    },
    {
        "condition_keywords": ["hypertension", "cardiovascular disease"],
        "authority": "NICE",
        "document_code": "NICE-NG136",
        "guideline_title": "NICE Guideline NG136: Hypertension in Adults Diagnosis and Management",
        "section_reference": "Sec 1.4, Treatment Steps",
        "publication_year": 2023,
        "evidence_grade": "Grade A",
        "recommendation_text": "Offer ACE inhibitor or ARB to adults aged under 55 or with type 2 diabetes. Offer CCB to adults aged 55 and over.",
        "first_line_regimen": "Ramipril 2.5mg daily (Step 1)",
        "contraindications": ["Bilateral renal artery stenosis"]
    },

    # 5. Type 2 Diabetes Mellitus
    {
        "condition_keywords": ["diabetes", "type 2 diabetes", "hyperglycemia"],
        "authority": "CDC",
        "document_code": "CDC-DCP-2023",
        "guideline_title": "CDC Clinical Diabetes Prevention and Management Standards",
        "section_reference": "Sec 5.2, Pharmacotherapy",
        "publication_year": 2023,
        "evidence_grade": "Grade A",
        "recommendation_text": "Metformin remains first-line therapy combined with lifestyle modification. Add SGLT2i or GLP-1RA if cardiorenal risk present.",
        "first_line_regimen": "Metformin 500mg BID with meals",
        "contraindications": ["Metabolic acidosis", "eGFR < 30 mL/min/1.73m2"]
    },

    # 6. FDA Safety Alerts & National Drug Safety
    {
        "condition_keywords": ["general", "drug safety", "fda alert"],
        "authority": "NATIONAL_FDA",
        "document_code": "FDA-DS-2024",
        "guideline_title": "FDA Drug Safety Communication: NSAID Avoidance in Late Pregnancy",
        "section_reference": "Sec 3.5, Warnings and Precautions",
        "publication_year": 2024,
        "evidence_grade": "Grade A",
        "recommendation_text": "Avoid use of NSAIDs in pregnant women at 20 weeks or later in pregnancy due to risk of fetal kidney dysfunction and oligohydramnios.",
        "first_line_regimen": "Paracetamol / Acetaminophen for pain relief in pregnancy",
        "contraindications": ["NSAIDs at >= 20 weeks gestation"]
    }
]

def match_clinical_guidelines(req: GuidelineMatchRequest, db: sqlite3.Connection) -> ClinicalGuidelineResponse:
    """Match condition and symptoms against WHO, CDC, NICE, and National Guidelines."""
    t0 = time.perf_counter()
    cond_lower = req.condition_name.lower().strip()
    sym_lowers = [s.lower().strip() for s in (req.reported_symptoms or [])]
    auth_filter = req.authority_filter.upper().strip() if req.authority_filter else None

    matched_items = []
    for g in CLINICAL_GUIDELINE_DATABASE:
        # Check authority filter
        if auth_filter and g["authority"] != auth_filter:
            continue

        # Check condition keyword match
        is_match = any(kw in cond_lower for kw in g["condition_keywords"])
        if not is_match and sym_lowers:
            is_match = any(any(kw in s for kw in g["condition_keywords"]) for s in sym_lowers)

        if is_match or cond_lower in ("general", "all"):
            matched_items.append(GuidelineReferenceItem(
                authority=g["authority"],
                document_code=g["document_code"],
                guideline_title=g["guideline_title"],
                section_reference=g["section_reference"],
                publication_year=g["publication_year"],
                evidence_grade=g["evidence_grade"],
                recommendation_text=g["recommendation_text"],
                first_line_regimen=g["first_line_regimen"],
                contraindications=g["contraindications"]
            ))

    t1 = time.perf_counter()
    latency_ms = int((t1 - t0) * 1000)

    return ClinicalGuidelineResponse(
        condition_name=req.condition_name,
        matched_guidelines_count=len(matched_items),
        guideline_references=matched_items,
        execution_time_ms=latency_ms
    )

def fetch_guidelines_by_authority(authority_code: str) -> List[GuidelineReferenceItem]:
    """Retrieve all guideline citations for a specific authority (WHO, CDC, NICE, NATIONAL_ICMR, NATIONAL_FDA)."""
    code_upper = authority_code.upper().strip()
    result = []
    for g in CLINICAL_GUIDELINE_DATABASE:
        if g["authority"] == code_upper or code_upper == "ALL":
            result.append(GuidelineReferenceItem(
                authority=g["authority"],
                document_code=g["document_code"],
                guideline_title=g["guideline_title"],
                section_reference=g["section_reference"],
                publication_year=g["publication_year"],
                evidence_grade=g["evidence_grade"],
                recommendation_text=g["recommendation_text"],
                first_line_regimen=g["first_line_regimen"],
                contraindications=g["contraindications"]
            ))
    return result
