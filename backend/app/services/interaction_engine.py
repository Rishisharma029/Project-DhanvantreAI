import sqlite3
from typing import List, Dict, Any, Optional
from itertools import combinations
from app.schemas.interaction_schema import (
    DrugInteractionItem, InteractionCheckResponse, CurrentVsRecommendedResponse
)

def get_severity_icon(sev: str) -> str:
    s_lower = (sev or "").lower()
    if 'major' in s_lower or 'dangerous' in s_lower or '🔴' in s_lower:
        return "🔴 Major"
    elif 'mod' in s_lower or 'caution' in s_lower or '🟡' in s_lower:
        return "🟡 Moderate"
    elif 'minor' in s_lower or 'safe' in s_lower or '🟢' in s_lower:
        return "🟢 Minor"
    return "🟢 Safe"

def get_severity_rank(sev: str) -> int:
    s_lower = (sev or "").lower()
    if 'major' in s_lower or 'dangerous' in s_lower or '🔴' in s_lower:
        return 3
    elif 'mod' in s_lower or 'caution' in s_lower or '🟡' in s_lower:
        return 2
    elif 'minor' in s_lower or 'safe' in s_lower or '🟢' in s_lower:
        return 1
    return 0

def resolve_drug_ingredients(drug_name: str, db: sqlite3.Connection) -> List[str]:
    """Resolve active ingredient names for a medicine or fallback to input string."""
    d_clean = drug_name.strip().lower()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT DISTINCT ingredient_name 
        FROM medicine_ingredients mi
        JOIN medicines m ON mi.medicine_id = m.id
        WHERE LOWER(m.canonical_name) LIKE ? OR LOWER(m.brand_name) LIKE ?;
    """, (f"%{d_clean}%", f"%{d_clean}%"))
    ings = [r[0] for r in cursor.fetchall()]
    
    if ings:
        return ings
    return [drug_name]

def query_single_pair_db(drug_a: str, drug_b: str, db: sqlite3.Connection) -> Optional[DrugInteractionItem]:
    """Query Phase 1 drug_interactions database for a pair of drug names/ingredients."""
    da = drug_a.strip().lower()
    db_term = drug_b.strip().lower()
    
    cursor = db.cursor()
    cursor.execute("""
        SELECT drug_a_name, drug_b_name, severity, interaction_description
        FROM drug_interactions
        WHERE (LOWER(drug_a_name) LIKE ? AND LOWER(drug_b_name) LIKE ?)
           OR (LOWER(drug_a_name) LIKE ? AND LOWER(drug_b_name) LIKE ?)
        LIMIT 1;
    """, (f"%{da}%", f"%{db_term}%", f"%{db_term}%", f"%{da}%"))
    
    row = cursor.fetchone()
    if row:
        d_a_name, d_b_name, sev, desc = row
        return DrugInteractionItem(
            drug_a=drug_a,
            drug_b=drug_b,
            severity=sev or "Moderate",
            severity_icon=get_severity_icon(sev or "Moderate"),
            description=desc or f"Interaction detected between {drug_a} and {drug_b}.",
            risk_level=get_severity_rank(sev or "Moderate")
        )
    return None

def check_pairwise_interaction(drug_a: str, drug_b: str, db: sqlite3.Connection) -> InteractionCheckResponse:
    """Check pairwise interaction between Drug A and Drug B."""
    match = query_single_pair_db(drug_a, drug_b, db)
    if match:
        return InteractionCheckResponse(
            has_interactions=True,
            highest_severity=match.severity,
            total_interactions_found=1,
            interactions=[match]
        )

    ings_a = resolve_drug_ingredients(drug_a, db)
    ings_b = resolve_drug_ingredients(drug_b, db)

    for ing1 in ings_a:
        for ing2 in ings_b:
            ing_match = query_single_pair_db(ing1, ing2, db)
            if ing_match:
                ing_match.drug_a = drug_a
                ing_match.drug_b = drug_b
                return InteractionCheckResponse(
                    has_interactions=True,
                    highest_severity=ing_match.severity,
                    total_interactions_found=1,
                    interactions=[ing_match]
                )

    return InteractionCheckResponse(
        has_interactions=False,
        highest_severity="Safe",
        total_interactions_found=0,
        interactions=[]
    )

def check_regimen_interactions(medicines: List[str], db: sqlite3.Connection) -> InteractionCheckResponse:
    """Check all pairwise combinations in a multi-drug regimen."""
    unique_meds = list(set(m.strip() for m in medicines if m.strip()))
    if len(unique_meds) < 2:
        return InteractionCheckResponse(has_interactions=False, highest_severity="Safe", total_interactions_found=0, interactions=[])

    interactions_found = []
    max_rank = 0
    highest_sev = "Safe"

    for med1, med2 in combinations(unique_meds, 2):
        pair_res = check_pairwise_interaction(med1, med2, db)
        if pair_res.has_interactions:
            for item in pair_res.interactions:
                interactions_found.append(item)
                if item.risk_level > max_rank:
                    max_rank = item.risk_level
                    highest_sev = item.severity

    return InteractionCheckResponse(
        has_interactions=len(interactions_found) > 0,
        highest_severity=highest_sev,
        total_interactions_found=len(interactions_found),
        interactions=interactions_found
    )

def check_current_vs_recommended(
    current_medicines: List[str],
    recommended_medicines: List[str],
    db: sqlite3.Connection
) -> CurrentVsRecommendedResponse:
    """
    Cross-check patient's current medications against newly recommended drugs.
    """
    clean_current = [m.strip() for m in current_medicines if m.strip()]
    clean_recommended = [m.strip() for m in recommended_medicines if m.strip()]

    conflicts = []
    max_rank = 0
    highest_sev = "Safe"

    for cur_med in clean_current:
        for rec_med in clean_recommended:
            if cur_med.lower() == rec_med.lower():
                item = DrugInteractionItem(
                    drug_a=cur_med,
                    drug_b=rec_med,
                    severity="Moderate",
                    severity_icon="🟡 Moderate",
                    description=f"Duplicate drug alert: Patient is already currently taking '{cur_med}'.",
                    risk_level=2
                )
                conflicts.append(item)
                if item.risk_level > max_rank:
                    max_rank = item.risk_level
                    highest_sev = item.severity
            else:
                pair_res = check_pairwise_interaction(cur_med, rec_med, db)
                if pair_res.has_interactions:
                    for item in pair_res.interactions:
                        conflicts.append(item)
                        if item.risk_level > max_rank:
                            max_rank = item.risk_level
                            highest_sev = item.severity

    return CurrentVsRecommendedResponse(
        has_conflicts=len(conflicts) > 0,
        highest_severity=highest_sev,
        total_conflicts_found=len(conflicts),
        conflicts=conflicts
    )
