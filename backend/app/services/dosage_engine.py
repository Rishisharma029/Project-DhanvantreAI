import re
import sqlite3
from typing import Optional, Dict, Any
from app.schemas.dosage_schema import DosageReferenceResponse

KNOWN_DOSAGE_RULES = {
    'paracetamol': {
        'adult': '500 mg - 650 mg per dose',
        'pediatric': '10 - 15 mg/kg per dose every 4-6 hours (Max 5 doses/24 hours)',
        'max_daily': '4000 mg (4 grams) per 24 hours',
        'route': 'Oral',
        'frequency': 'Every 4 - 6 hours as needed (PRN)',
        'duration': '3 - 5 days (Seek physician if fever persists > 3 days)'
    },
    'acetaminophen': {
        'adult': '500 mg - 650 mg per dose',
        'pediatric': '10 - 15 mg/kg per dose every 4-6 hours',
        'max_daily': '4000 mg (4 grams) per 24 hours',
        'route': 'Oral',
        'frequency': 'Every 4 - 6 hours PRN',
        'duration': '3 - 5 days'
    },
    'amoxycillin': {
        'adult': '500 mg - 875 mg per dose',
        'pediatric': '20 - 45 mg/kg/day divided in 2 to 3 doses',
        'max_daily': '3000 mg (3 grams) per 24 hours',
        'route': 'Oral',
        'frequency': 'Every 8 - 12 hours (BID / TID)',
        'duration': '5 - 10 days (Complete full antibiotic course)'
    },
    'azithromycin': {
        'adult': '500 mg on Day 1, followed by 250 mg once daily on Days 2-5',
        'pediatric': '10 mg/kg on Day 1, followed by 5 mg/kg once daily on Days 2-5',
        'max_daily': '500 mg per 24 hours',
        'route': 'Oral',
        'frequency': 'Once daily (QD)',
        'duration': '3 - 5 days'
    },
    'ibuprofen': {
        'adult': '200 mg - 400 mg per dose',
        'pediatric': '5 - 10 mg/kg per dose every 6-8 hours',
        'max_daily': '1200 mg (OTC) / 3200 mg (Prescription maximum)',
        'route': 'Oral',
        'frequency': 'Every 6 - 8 hours as needed with food',
        'duration': '3 - 5 days'
    },
    'fluconazole': {
        'adult': '150 mg single dose for cutaneous/vaginal candidiasis; 200 - 400 mg daily for systemic infections',
        'pediatric': '3 - 6 mg/kg once daily under medical supervision',
        'max_daily': '400 mg per 24 hours',
        'route': 'Oral',
        'frequency': 'Single dose or Once daily (QD)',
        'duration': '1 day (single dose) to 14 days depending on indication'
    },
    'metformin': {
        'adult': '500 mg - 850 mg twice daily with meals',
        'pediatric': '500 mg once or twice daily (Age 10+ only)',
        'max_daily': '2550 mg per 24 hours',
        'route': 'Oral',
        'frequency': 'Twice daily (BID) with meals',
        'duration': 'Long-term chronic therapy'
    },
    'amlodipine': {
        'adult': '5 mg once daily, may increase to 10 mg once daily',
        'pediatric': '2.5 mg to 5 mg once daily (Age 6-17 years)',
        'max_daily': '10 mg per 24 hours',
        'route': 'Oral',
        'frequency': 'Once daily (QD)',
        'duration': 'Long-term maintenance therapy'
    }
}

def extract_dosage_reference(medicine_name: str, medicine_id: Optional[int], db: sqlite3.Connection) -> DosageReferenceResponse:
    """
    Retrieve structured clinical dosage reference for a medicine.
    """
    cursor = db.cursor()
    m_row = None
    
    if medicine_id:
        cursor.execute("SELECT id, canonical_name, generic_name, composition FROM medicines WHERE id = ?;", (medicine_id,))
        m_row = cursor.fetchone()
        
    if not m_row:
        clean_q = medicine_name.strip().lower()
        cursor.execute("""
            SELECT id, canonical_name, generic_name, composition 
            FROM medicines 
            WHERE LOWER(canonical_name) LIKE ? OR LOWER(brand_name) LIKE ?
            LIMIT 1;
        """, (f"%{clean_q}%", f"%{clean_q}%"))
        m_row = cursor.fetchone()

    canonical_name = m_row["canonical_name"] if m_row else medicine_name
    generic_name = m_row["generic_name"] if m_row else None
    composition = m_row["composition"] if m_row else None

    # Determine matched key
    search_space = f"{canonical_name} {generic_name or ''} {composition or ''} {medicine_name}".lower()
    matched_rule = None
    for k, rule in KNOWN_DOSAGE_RULES.items():
        if k in search_space:
            matched_rule = rule
            break

    # Determine Route
    route = "Oral"
    if any(term in search_space for term in ['cream', 'ointment', 'gel', 'lotion']):
        route = "Topical"
    elif any(term in search_space for term in ['injection', 'iv', 'infusion']):
        route = "Intravenous / Intramuscular"
    elif any(term in search_space for term in ['drop', 'eye', 'ear', 'ophthalmic']):
        route = "Ophthalmic / Otic"

    if matched_rule:
        return DosageReferenceResponse(
            medicine_name=canonical_name,
            generic_name=generic_name,
            composition=composition,
            standard_adult_dose=matched_rule['adult'],
            pediatric_dose=matched_rule['pediatric'],
            maximum_daily_dose=matched_rule['max_daily'],
            route=matched_rule['route'] or route,
            frequency=matched_rule['frequency'],
            duration=matched_rule['duration']
        )

    # Fallback derivation from parsed dosage numbers in composition
    dose_numbers = re.findall(r'(\d+(?:\.\d+)?\s*(?:mg|g|mcg|ml))', search_space)
    primary_strength = dose_numbers[0] if dose_numbers else "Standard strength per label"

    return DosageReferenceResponse(
        medicine_name=canonical_name,
        generic_name=generic_name,
        composition=composition,
        standard_adult_dose=f"1 unit ({primary_strength}) per dose",
        pediatric_dose="Weight-based pediatric dosing; consult pediatrician before administration",
        maximum_daily_dose=f"3 to 4 doses ({primary_strength} equivalent) per 24 hours",
        route=route,
        frequency="Every 8 - 12 hours as prescribed",
        duration="5 - 7 days or as directed by treating physician"
    )
