import sqlite3
from typing import List, Dict, Any
from app.schemas.universal_search_schema import (
    SearchResultItem, UniversalSearchResponse
)

def execute_universal_search(query: str, domain: str = "all", limit: int = 20, db: sqlite3.Connection = None) -> UniversalSearchResponse:
    """
    Executes Universal Search across 5 clinical domains:
    1. Medicines
    2. Diseases
    3. Symptoms
    4. Ingredients
    5. Manufacturers
    """
    clean_q = query.strip().lower()
    pattern = f"%{clean_q}%"
    domain_clean = (domain or "all").strip().lower()
    cursor = db.cursor()

    results_by_cat: Dict[str, List[SearchResultItem]] = {
        "Medicine": [],
        "Disease": [],
        "Symptom": [],
        "Ingredient": [],
        "Manufacturer": []
    }
    all_items: List[SearchResultItem] = []

    # 1. MEDICINES SEARCH
    if domain_clean in ["all", "medicines", "medicine"]:
        cursor.execute("""
            SELECT id, canonical_name, brand_name, generic_name, composition, price_inr
            FROM medicines
            WHERE LOWER(canonical_name) LIKE ? OR LOWER(brand_name) LIKE ? OR LOWER(generic_name) LIKE ?
            LIMIT ?;
        """, (pattern, pattern, pattern, limit))
        for row in cursor.fetchall():
            item = SearchResultItem(
                id=row[0],
                category="Medicine",
                title=row[1] or row[2],
                subtitle=f"Generic: {row[3]}" if row[3] else f"Brand: {row[2]}",
                description_snippet=f"Composition: {row[4]} | Price: ₹{row[5]}",
                relevance_score=0.95 if clean_q in (row[1] or "").lower() else 0.80,
                metadata={"price_inr": row[5], "generic_name": row[3]}
            )
            results_by_cat["Medicine"].append(item)
            all_items.append(item)

    # 2. DISEASES SEARCH
    if domain_clean in ["all", "diseases", "disease"]:
        cursor.execute("""
            SELECT id, name, severity_level, description
            FROM diseases
            WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ?
            LIMIT ?;
        """, (pattern, pattern, limit))
        for row in cursor.fetchall():
            item = SearchResultItem(
                id=row[0],
                category="Disease",
                title=row[1],
                subtitle=f"Severity: {row[2]}",
                description_snippet=row[3][:150] + "..." if row[3] and len(row[3]) > 150 else row[3],
                relevance_score=0.95 if clean_q in row[1].lower() else 0.75,
                metadata={"severity": row[2]}
            )
            results_by_cat["Disease"].append(item)
            all_items.append(item)

    # 3. SYMPTOMS SEARCH
    if domain_clean in ["all", "symptoms", "symptom"]:
        cursor.execute("""
            SELECT id, name
            FROM symptoms
            WHERE LOWER(name) LIKE ?
            LIMIT ?;
        """, (pattern, limit))
        for row in cursor.fetchall():
            item = SearchResultItem(
                id=row[0],
                category="Symptom",
                title=row[1].title(),
                subtitle="Clinical Symptom Entity",
                description_snippet=f"Clinical presentation matching '{row[1]}'",
                relevance_score=0.90 if clean_q == row[1].lower() else 0.80,
                metadata={}
            )
            results_by_cat["Symptom"].append(item)
            all_items.append(item)

    # 4. INGREDIENTS SEARCH
    if domain_clean in ["all", "ingredients", "ingredient"]:
        cursor.execute("""
            SELECT id, ingredient_name
            FROM medicine_ingredients
            WHERE LOWER(ingredient_name) LIKE ?
            LIMIT ?;
        """, (pattern, limit))
        for row in cursor.fetchall():
            item = SearchResultItem(
                id=row[0],
                category="Ingredient",
                title=row[1].title(),
                subtitle="Active Pharmaceutical Ingredient",
                description_snippet=f"Active substance component: {row[1]}",
                relevance_score=0.85,
                metadata={}
            )
            results_by_cat["Ingredient"].append(item)
            all_items.append(item)

    # 5. MANUFACTURERS SEARCH
    if domain_clean in ["all", "manufacturers", "manufacturer"]:
        cursor.execute("""
            SELECT id, name
            FROM manufacturers
            WHERE LOWER(name) LIKE ?
            LIMIT ?;
        """, (pattern, limit))
        for row in cursor.fetchall():
            item = SearchResultItem(
                id=row[0],
                category="Manufacturer",
                title=row[1],
                subtitle="Pharma Manufacturer / Company",
                description_snippet=f"Pharmaceutical producer: {row[1]}",
                relevance_score=0.85,
                metadata={}
            )
            results_by_cat["Manufacturer"].append(item)
            all_items.append(item)

    categories_found = [cat for cat, items in results_by_cat.items() if len(items) > 0]

    return UniversalSearchResponse(
        query=query,
        domain_filter=domain,
        total_results=len(all_items),
        categories_found=categories_found,
        results_by_category={k: v for k, v in results_by_cat.items() if len(v) > 0},
        all_results=all_items[:limit*2]
    )
