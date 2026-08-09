import sqlite3
from typing import List, Dict, Any, Optional
from app.schemas.knowledge_schema import (
    Disease360KnowledgeResponse, Medicine360KnowledgeResponse,
    DietItem, PrecautionItem, WorkoutItem, SideEffectInfo, InteractionInfo
)
from app.services.interaction_engine import get_severity_icon

def fetch_disease_360(identifier: str, db: sqlite3.Connection) -> Optional[Disease360KnowledgeResponse]:
    """Retrieve 360° Knowledge Profile for a Disease (Symptoms, Diets, Precautions, Workouts)."""
    cursor = db.cursor()
    d_row = None
    
    if identifier.isdigit():
        cursor.execute("SELECT id, name, severity_level, description FROM diseases WHERE id = ?;", (int(identifier),))
        d_row = cursor.fetchone()

    if not d_row:
        cursor.execute("""
            SELECT id, name, severity_level, description 
            FROM diseases 
            WHERE LOWER(name) LIKE ? 
            LIMIT 1;
        """, (f"%{identifier.strip().lower()}%",))
        d_row = cursor.fetchone()

    if not d_row:
        return None

    d_id, d_name, d_sev, d_desc = d_row

    # 1. Symptoms
    cursor.execute("""
        SELECT s.name 
        FROM symptoms s
        JOIN disease_symptoms ds ON s.id = ds.symptom_id
        WHERE ds.disease_id = ?;
    """, (d_id,))
    symptoms = [r[0].title() for r in cursor.fetchall()]

    # 2. Diets
    cursor.execute("SELECT diet FROM disease_diets WHERE disease_id = ?;", (d_id,))
    diets = [r[0] for r in cursor.fetchall()]

    # 3. Precautions
    cursor.execute("SELECT precaution FROM disease_precautions WHERE disease_id = ?;", (d_id,))
    precautions = [r[0] for r in cursor.fetchall()]

    # 4. Workouts
    cursor.execute("SELECT workout FROM disease_workouts WHERE disease_id = ?;", (d_id,))
    workouts = [r[0] for r in cursor.fetchall()]

    return Disease360KnowledgeResponse(
        disease_id=d_id,
        disease_name=d_name,
        severity_level=d_sev or "Moderate",
        description=d_desc or "",
        symptoms=symptoms,
        diets=diets,
        precautions=precautions,
        workouts=workouts
    )

def fetch_medicine_360(identifier: str, db: sqlite3.Connection) -> Optional[Medicine360KnowledgeResponse]:
    """Retrieve 360° Knowledge Profile for a Medicine (Ingredients, Side Effects, Interactions, Uses, Substitutes)."""
    cursor = db.cursor()
    m_row = None

    if identifier.isdigit():
        cursor.execute("""
            SELECT m.*, mfg.name as mfg_name 
            FROM medicines m 
            LEFT JOIN manufacturers mfg ON m.manufacturer_id = mfg.id 
            WHERE m.id = ?;
        """, (int(identifier),))
        m_row = cursor.fetchone()

    if not m_row:
        cursor.execute("""
            SELECT m.*, mfg.name as mfg_name 
            FROM medicines m 
            LEFT JOIN manufacturers mfg ON m.manufacturer_id = mfg.id 
            WHERE LOWER(m.canonical_name) LIKE ? OR LOWER(m.brand_name) LIKE ?
            LIMIT 1;
        """, (f"%{identifier.strip().lower()}%", f"%{identifier.strip().lower()}%"))
        m_row = cursor.fetchone()

    if not m_row:
        return None

    r = dict(m_row)
    m_id = r["id"]

    # 1. Ingredients
    cursor.execute("SELECT ingredient_name FROM medicine_ingredients WHERE medicine_id = ?;", (m_id,))
    ingredients = [ing[0] for ing in cursor.fetchall()]

    # 2. Side Effects
    cursor.execute("SELECT side_effect_name, frequency FROM side_effects WHERE medicine_id = ? LIMIT 20;", (m_id,))
    side_effects = [SideEffectInfo(medicine_name=r["canonical_name"], side_effect_name=se[0], frequency=se[1] or "Common") for se in cursor.fetchall()]

    # 3. Interactions
    cursor.execute("""
        SELECT drug_a_name, drug_b_name, severity, interaction_description
        FROM drug_interactions
        WHERE LOWER(drug_a_name) LIKE ? OR LOWER(drug_b_name) LIKE ?
        LIMIT 20;
    """, (f"%{r['canonical_name'].lower()}%", f"%{r['canonical_name'].lower()}%"))
    interactions = []
    for row in cursor.fetchall():
        da, db_name, sev, desc = row
        interactions.append(InteractionInfo(
            drug_a=da,
            drug_b=db_name,
            severity=sev or "Moderate",
            severity_icon=get_severity_icon(sev or "Moderate"),
            description=desc or ""
        ))

    # 4. Uses
    cursor.execute("SELECT use_name FROM medicine_uses WHERE medicine_id = ? LIMIT 20;", (m_id,))
    uses = [u[0] for u in cursor.fetchall()]

    # 5. Substitutes
    cursor.execute("SELECT substitute_name FROM substitutes WHERE medicine_id = ? LIMIT 20;", (m_id,))
    substitutes = [s[0] for s in cursor.fetchall()]

    return Medicine360KnowledgeResponse(
        medicine_id=m_id,
        canonical_name=r["canonical_name"],
        brand_name=r["brand_name"],
        generic_name=r.get("generic_name"),
        composition=r.get("composition"),
        price_inr=r.get("price_inr"),
        manufacturer_name=r.get("mfg_name"),
        ingredients=ingredients,
        side_effects=side_effects,
        interactions=interactions,
        uses=uses,
        substitutes=substitutes
    )

def fetch_diets_by_disease(disease_name: str, db: sqlite3.Connection) -> List[DietItem]:
    """Retrieve recommended dietary guidelines for a disease."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT d.name, dd.diet
        FROM disease_diets dd
        JOIN diseases d ON dd.disease_id = d.id
        WHERE LOWER(d.name) LIKE ?;
    """, (f"%{disease_name.strip().lower()}%",))
    return [DietItem(disease_name=r[0], diet_recommendation=r[1]) for r in cursor.fetchall()]

def fetch_precautions_by_disease(disease_name: str, db: sqlite3.Connection) -> List[PrecautionItem]:
    """Retrieve clinical precautions for a disease."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT d.name, dp.precaution
        FROM disease_precautions dp
        JOIN diseases d ON dp.disease_id = d.id
        WHERE LOWER(d.name) LIKE ?;
    """, (f"%{disease_name.strip().lower()}%",))
    return [PrecautionItem(disease_name=r[0], precaution=r[1]) for r in cursor.fetchall()]

def fetch_workouts_by_disease(disease_name: str, db: sqlite3.Connection) -> List[WorkoutItem]:
    """Retrieve exercise and workout recommendations for a disease."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT d.name, dw.workout
        FROM disease_workouts dw
        JOIN diseases d ON dw.disease_id = d.id
        WHERE LOWER(d.name) LIKE ?;
    """, (f"%{disease_name.strip().lower()}%",))
    return [WorkoutItem(disease_name=r[0], workout_recommendation=r[1]) for r in cursor.fetchall()]
