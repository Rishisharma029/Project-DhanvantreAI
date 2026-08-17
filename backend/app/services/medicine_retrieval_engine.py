import sqlite3
from typing import List, Dict, Any, Optional
from app.schemas.medicine_schema import (
    MedicineSummary, MedicineDetailResponse, IngredientItem,
    SubstituteItem, MedicineSearchResponse
)

def search_medicines(
    query: str,
    search_by: str = "all", # all, name, generic, brand, ingredient, use
    page: int = 1,
    limit: int = 20,
    db: sqlite3.Connection = None
) -> MedicineSearchResponse:
    """
    Search medicines across canonical name, brand name, generic name, composition, ingredients, or uses.
    """
    query = query.replace("<", "&lt;").replace(">", "&gt;")
    q_clean = query.strip()
    if not q_clean:
        return MedicineSearchResponse(query=query, search_by=search_by, page=page, limit=limit, total_results=0, medicines=[])

    offset = (page - 1) * limit
    cursor = db.cursor()
    pattern = f"%{q_clean.lower()}%"

    where_clause = ""
    params = []

    if search_by == "name" or search_by == "brand":
        where_clause = "WHERE LOWER(m.canonical_name) LIKE ? OR LOWER(m.brand_name) LIKE ?"
        params = [pattern, pattern]
    elif search_by == "generic":
        where_clause = "WHERE LOWER(m.generic_name) LIKE ?"
        params = [pattern]
    elif search_by == "ingredient":
        where_clause = "WHERE m.id IN (SELECT medicine_id FROM medicine_ingredients WHERE LOWER(ingredient_name) LIKE ?)"
        params = [pattern]
    elif search_by == "use":
        where_clause = "WHERE m.id IN (SELECT medicine_id FROM medicine_uses WHERE LOWER(use_name) LIKE ?)"
        params = [pattern]
    else: # "all"
        where_clause = """
            WHERE LOWER(m.canonical_name) LIKE ?
               OR LOWER(m.brand_name) LIKE ?
               OR LOWER(m.generic_name) LIKE ?
               OR LOWER(m.composition) LIKE ?
               OR m.id IN (SELECT medicine_id FROM medicine_ingredients WHERE LOWER(ingredient_name) LIKE ?)
               OR m.id IN (SELECT medicine_id FROM medicine_uses WHERE LOWER(use_name) LIKE ?)
        """
        params = [pattern, pattern, pattern, pattern, pattern, pattern]

    # Count Query
    count_sql = f"SELECT COUNT(*) FROM medicines m {where_clause};"
    cursor.execute(count_sql, params)
    total_results = cursor.fetchone()[0]

    # Data Query
    select_sql = f"""
        SELECT m.id, m.canonical_name, m.brand_name, m.generic_name, m.price_inr,
               m.is_discontinued, m.pack_size_label, m.composition, m.type, mfg.name as mfg_name
        FROM medicines m
        LEFT JOIN manufacturers mfg ON m.manufacturer_id = mfg.id
        {where_clause}
        ORDER BY m.id ASC
        LIMIT ? OFFSET ?;
    """
    cursor.execute(select_sql, params + [limit, offset])
    rows = cursor.fetchall()

    medicines = []
    for r in rows:
        medicines.append(MedicineSummary(
            id=r["id"],
            canonical_name=r["canonical_name"],
            brand_name=r["brand_name"],
            generic_name=r["generic_name"],
            price_inr=r["price_inr"],
            is_discontinued=bool(r["is_discontinued"]),
            pack_size_label=r["pack_size_label"],
            composition=r["composition"],
            type=r["type"] or "allopathy",
            manufacturer_name=r["mfg_name"]
        ))

    return MedicineSearchResponse(
        query=query,
        search_by=search_by,
        page=page,
        limit=limit,
        total_results=total_results,
        medicines=medicines
    )

def get_medicine_details(medicine_id: int, db: sqlite3.Connection) -> Optional[MedicineDetailResponse]:
    """Retrieve complete medicine detail record."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.*, mfg.name as mfg_name
        FROM medicines m
        LEFT JOIN manufacturers mfg ON m.manufacturer_id = mfg.id
        WHERE m.id = ?;
    """, (medicine_id,))
    row = cursor.fetchone()
    if not row:
        return None

    r = dict(row)

    # 1. Ingredients
    cursor.execute("SELECT ingredient_name, strength, unit FROM medicine_ingredients WHERE medicine_id = ?;", (medicine_id,))
    ingredients = [IngredientItem(ingredient_name=ir[0], strength=ir[1], unit=ir[2]) for ir in cursor.fetchall()]

    # 2. Aliases
    cursor.execute("SELECT alias_name FROM medicine_aliases WHERE medicine_id = ?;", (medicine_id,))
    aliases = [ar[0] for ar in cursor.fetchall()]

    # 3. Side Effects
    cursor.execute("SELECT side_effect_name FROM side_effects WHERE medicine_id = ? LIMIT 20;", (medicine_id,))
    side_effects = [se[0] for se in cursor.fetchall()]

    # 4. Uses
    cursor.execute("SELECT use_name FROM medicine_uses WHERE medicine_id = ? LIMIT 20;", (medicine_id,))
    uses = [u[0] for u in cursor.fetchall()]

    # 5. Substitutes
    substitutes = get_medicine_substitutes(medicine_id, db)

    return MedicineDetailResponse(
        id=r["id"],
        canonical_name=r["canonical_name"],
        brand_name=r["brand_name"],
        generic_name=r["generic_name"],
        price_inr=r["price_inr"],
        is_discontinued=bool(r["is_discontinued"]),
        pack_size_label=r["pack_size_label"],
        composition=r["composition"],
        type=r["type"] or "allopathy",
        manufacturer_name=r["mfg_name"],
        pregnancy_category=r.get("pregnancy_category"),
        alcohol_warning=r.get("alcohol_warning"),
        csa_schedule=r.get("csa_schedule"),
        rx_otc=r.get("rx_otc"),
        ingredients=ingredients,
        aliases=aliases,
        side_effects=side_effects,
        uses=uses,
        substitutes=substitutes
    )

def get_medicine_substitutes(medicine_id: int, db: sqlite3.Connection) -> List[SubstituteItem]:
    """Retrieve substitute alternative medicines for a given medicine ID."""
    cursor = db.cursor()
    cursor.execute("""
        SELECT s.substitute_name, s.substitute_medicine_id, m.price_inr, mfg.name as mfg_name
        FROM substitutes s
        LEFT JOIN medicines m ON s.substitute_medicine_id = m.id
        LEFT JOIN manufacturers mfg ON m.manufacturer_id = mfg.id
        WHERE s.medicine_id = ?
        LIMIT 20;
    """, (medicine_id,))
    
    subs = []
    for r in cursor.fetchall():
        subs.append(SubstituteItem(
            substitute_name=r["substitute_name"],
            substitute_medicine_id=r["substitute_medicine_id"],
            price_inr=r["price_inr"],
            manufacturer_name=r["mfg_name"]
        ))
    return subs
