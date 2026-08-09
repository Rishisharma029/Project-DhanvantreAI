import os
import csv
import re
import sqlite3
import time
from normalizer import (
    normalize_string, get_canonical_medicine_key, parse_composition,
    classify_interaction_severity, clean_price, clean_boolean,
    parse_list_str, clean_symptom_name, clean_disease_name
)

RAW_DATA_DIR = os.path.join(os.getcwd(), 'data', 'raw')
OUTPUT_DB = os.path.join(os.getcwd(), 'medical_database.db')
POSTGRES_DUMP = os.path.join(os.getcwd(), 'medical_db_dump.sql')

# Predefined Medical Synonyms Dictionary
INITIAL_SYNONYMS = [
    ('Tylenol', 'Paracetamol', 'drug_brand_to_generic'),
    ('Crocin', 'Paracetamol', 'drug_brand_to_generic'),
    ('Calpol', 'Paracetamol', 'drug_brand_to_generic'),
    ('Dolo', 'Paracetamol', 'drug_brand_to_generic'),
    ('Acetaminophen', 'Paracetamol', 'generic_synonym'),
    ('High BP', 'Hypertension', 'disease_lay_to_clinical'),
    ('Low BP', 'Hypotension', 'disease_lay_to_clinical'),
    ('Heart Attack', 'Myocardial Infarction', 'disease_lay_to_clinical'),
    ('Sugar', 'Diabetes Mellitus', 'disease_lay_to_clinical'),
    ('Diabetes', 'Diabetes Mellitus', 'disease_lay_to_clinical'),
    ('Fever', 'Pyrexia', 'disease_lay_to_clinical'),
    ('Stroke', 'Cerebrovascular Accident', 'disease_lay_to_clinical'),
    ('Flu', 'Influenza', 'disease_lay_to_clinical'),
    ('Fit', 'Seizure', 'disease_lay_to_clinical')
]

# Disease Severities
DISEASE_SEVERITIES = {
    'Heart Attack': 'Emergency',
    'Myocardial Infarction': 'Emergency',
    'Stroke': 'Emergency',
    'Paralysis (Brain Hemorrhage)': 'Emergency',
    'Pneumonia': 'Severe',
    'Tuberculosis': 'Severe',
    'Hepatitis B': 'Severe',
    'Hepatitis C': 'Severe',
    'Hepatitis D': 'Severe',
    'Hepatitis E': 'Severe',
    'Dengue': 'Severe',
    'Malaria': 'Severe',
    'Typhoid': 'Severe',
    'Diabetes': 'Moderate',
    'Hypertension': 'Moderate',
    'Hyperthyroidism': 'Moderate',
    'Hypothyroidism': 'Moderate',
    'Migraine': 'Moderate',
    'Jaundice': 'Moderate',
    'Fungal Infection': 'Mild',
    'Common Cold': 'Mild',
    'Acne': 'Mild',
    'Allergy': 'Mild',
    'Psoriasis': 'Mild'
}

def run_etl():
    print("=" * 65)
    print("Starting Phase 1.1 - 1.12 Data Engineering ETL Pipeline...")
    print("=" * 65)
    start_time = time.time()

    if os.path.exists(OUTPUT_DB):
        os.remove(OUTPUT_DB)
        
    conn = sqlite3.connect(OUTPUT_DB)
    cursor = conn.cursor()

    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = MEMORY;")
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("\n[Step 1/7] Creating Database Schema...")
    cursor.executescript("""
    CREATE TABLE manufacturers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        canonical_name TEXT NOT NULL,
        brand_name TEXT NOT NULL,
        generic_name TEXT,
        canonical_key TEXT NOT NULL,
        search_tokens TEXT,
        price_inr REAL,
        is_discontinued INTEGER DEFAULT 0,
        pack_size_label TEXT,
        composition TEXT,
        type TEXT,
        pregnancy_category TEXT,
        alcohol_warning TEXT,
        csa_schedule TEXT,
        rx_otc TEXT,
        manufacturer_id INTEGER,
        FOREIGN KEY(manufacturer_id) REFERENCES manufacturers(id) ON DELETE SET NULL
    );

    CREATE TABLE medicine_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER NOT NULL,
        ingredient_name TEXT NOT NULL,
        strength REAL,
        unit TEXT,
        FOREIGN KEY(medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    );

    CREATE TABLE medicine_aliases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER NOT NULL,
        alias_name TEXT NOT NULL,
        FOREIGN KEY(medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    );

    CREATE TABLE synonyms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_term TEXT NOT NULL,
        canonical_term TEXT NOT NULL,
        category TEXT DEFAULT 'general'
    );

    CREATE TABLE diseases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        severity_level TEXT DEFAULT 'Moderate',
        description TEXT,
        causes TEXT,
        risk_factors TEXT,
        complications TEXT,
        diagnosis TEXT,
        treatment TEXT
    );

    CREATE TABLE symptoms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        severity_weight INTEGER DEFAULT 1
    );

    CREATE TABLE disease_symptoms (
        disease_id INTEGER,
        symptom_id INTEGER,
        PRIMARY KEY(disease_id, symptom_id),
        FOREIGN KEY(disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
        FOREIGN KEY(symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
    );

    CREATE TABLE disease_precautions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_id INTEGER,
        precaution TEXT NOT NULL,
        FOREIGN KEY(disease_id) REFERENCES diseases(id) ON DELETE CASCADE
    );

    CREATE TABLE disease_diets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_id INTEGER,
        diet TEXT NOT NULL,
        FOREIGN KEY(disease_id) REFERENCES diseases(id) ON DELETE CASCADE
    );

    CREATE TABLE disease_workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_id INTEGER,
        workout TEXT NOT NULL,
        FOREIGN KEY(disease_id) REFERENCES diseases(id) ON DELETE CASCADE
    );

    CREATE TABLE drug_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_a_name TEXT NOT NULL,
        drug_b_name TEXT NOT NULL,
        drug_a_id INTEGER,
        drug_b_id INTEGER,
        severity TEXT DEFAULT 'Moderate',
        severity_tag TEXT DEFAULT '🟡 Caution',
        interaction_description TEXT NOT NULL,
        FOREIGN KEY(drug_a_id) REFERENCES medicines(id),
        FOREIGN KEY(drug_b_id) REFERENCES medicines(id)
    );

    CREATE TABLE side_effects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        side_effect_name TEXT NOT NULL,
        frequency TEXT DEFAULT 'Common',
        FOREIGN KEY(medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    );

    CREATE TABLE medicine_uses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        use_name TEXT NOT NULL,
        FOREIGN KEY(medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    );

    CREATE TABLE substitutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        substitute_name TEXT NOT NULL,
        substitute_medicine_id INTEGER,
        FOREIGN KEY(medicine_id) REFERENCES medicines(id) ON DELETE CASCADE,
        FOREIGN KEY(substitute_medicine_id) REFERENCES medicines(id)
    );
    """)
    conn.commit()

    # Seed Synonyms
    cursor.executemany("INSERT INTO synonyms (source_term, canonical_term, category) VALUES (?, ?, ?);", INITIAL_SYNONYMS)
    conn.commit()

    def read_csv(filename):
        filepath = os.path.join(RAW_DATA_DIR, filename)
        if not os.path.exists(filepath):
            return []
        with open(filepath, mode='r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            return list(reader)

    # Caches
    manufacturers_map = {} # name -> id
    canonical_med_map = {} # canonical_key -> medicine_id
    raw_name_to_id = {}    # raw_name.lower() -> medicine_id
    diseases_map = {}      # name -> id
    symptoms_map = {}      # name -> id

    # -------------------------------------------------------------
    # [Step 2/7] Process Manufacturers & Medicines (Canonical Deduplication)
    # -------------------------------------------------------------
    print("\n[Step 2/7] Processing Manufacturers & Canonical Medicines...")
    
    az_data = read_csv('A_Z_medicines_dataset_of_India.csv')
    print(f"  Loaded {len(az_data)} records from A_Z_medicines_dataset_of_India.csv")

    # Manufacturers
    mfg_set = set()
    for row in az_data:
        mfg = normalize_string(row.get('manufacturer_name', ''))
        if mfg: mfg_set.add(mfg)
            
    cursor.executemany("INSERT OR IGNORE INTO manufacturers (name) VALUES (?);", [(mfg,) for mfg in sorted(mfg_set)])
    conn.commit()

    cursor.execute("SELECT name, id FROM manufacturers;")
    for mfg_name, mfg_id in cursor.fetchall():
        manufacturers_map[mfg_name] = mfg_id

    ingredients_to_insert = []
    aliases_to_insert = []

    for row in az_data:
        raw_name = normalize_string(row.get('name', ''))
        if not raw_name or len(raw_name) < 2:
            continue # Phase 1.1 Data Quality Sanitation

        canon_key = get_canonical_medicine_key(raw_name)
        mfg_name = normalize_string(row.get('manufacturer_name', ''))
        mfg_id = manufacturers_map.get(mfg_name, None)
        price = clean_price(row.get('price(₹)', 0))
        is_disc = 1 if clean_boolean(row.get('Is_discontinued', False)) else 0
        pack_size = normalize_string(row.get('pack_size_label', ''))
        comp = normalize_string(row.get('short_composition1', ''))
        med_type = normalize_string(row.get('type', 'allopathy'))

        # Phase 1.3 Search tokens
        search_tokens = f"{raw_name} {canon_key} {comp}".strip().lower()

        if canon_key in canonical_med_map:
            # Duplicate brand variant mapping to existing canonical medicine
            med_id = canonical_med_map[canon_key]
            aliases_to_insert.append((med_id, raw_name))
            raw_name_to_id[raw_name.lower()] = med_id
        else:
            cursor.execute("""
                INSERT INTO medicines (canonical_name, brand_name, canonical_key, search_tokens, price_inr, is_discontinued, pack_size_label, composition, type, manufacturer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (raw_name, raw_name, canon_key, search_tokens, price, is_disc, pack_size, comp, med_type, mfg_id))
            med_id = cursor.lastrowid
            canonical_med_map[canon_key] = med_id
            raw_name_to_id[raw_name.lower()] = med_id

            # Phase 1.1 Composition Breakdown
            if comp:
                parsed_ings = parse_composition(comp)
                for ing in parsed_ings:
                    ingredients_to_insert.append((med_id, ing['ingredient'], ing['strength'], ing['unit']))

    conn.commit()
    print(f"  Deduplicated into {len(canonical_med_map)} unique canonical medicines.")

    # -------------------------------------------------------------
    # [Step 3/7] Supplementary Medicines, Uses, Side Effects, Substitutes
    # -------------------------------------------------------------
    print("\n[Step 3/7] Enriching Substitutes, Uses, Side Effects, & Drugs.com Data...")

    med_dataset = read_csv('medicine_dataset.csv')
    substitutes_records = []
    side_effects_records = []
    uses_records = []

    for row in med_dataset:
        raw_name = normalize_string(row.get('name', ''))
        if not raw_name: continue
        
        canon_key = get_canonical_medicine_key(raw_name)
        med_id = canonical_med_map.get(canon_key)
        
        if not med_id:
            search_tokens = f"{raw_name} {canon_key}".lower()
            cursor.execute("""
                INSERT INTO medicines (canonical_name, brand_name, canonical_key, search_tokens, type)
                VALUES (?, ?, ?, ?, 'allopathy');
            """, (raw_name, raw_name, canon_key, search_tokens))
            med_id = cursor.lastrowid
            canonical_med_map[canon_key] = med_id
            raw_name_to_id[raw_name.lower()] = med_id

        for i in range(5):
            sub_val = normalize_string(row.get(f'substitute{i}', ''))
            if sub_val:
                sub_ckey = get_canonical_medicine_key(sub_val)
                sub_med_id = canonical_med_map.get(sub_ckey)
                substitutes_records.append((med_id, sub_val, sub_med_id))

        for i in range(5):
            se_val = normalize_string(row.get(f'sideEffect{i}', ''))
            if se_val:
                side_effects_records.append((med_id, se_val, 'Common'))

        for i in range(5):
            u_val = normalize_string(row.get(f'use{i}', ''))
            if u_val:
                uses_records.append((med_id, u_val))

    # Drugs.com
    drugs_com_data = read_csv('drugs_side_effects_drugs_com.csv')
    for row in drugs_com_data:
        drug_name = normalize_string(row.get('drug_name', ''))
        if not drug_name: continue
        
        generic_name = normalize_string(row.get('generic_name', ''))
        preg_cat = normalize_string(row.get('pregnancy_category', ''))
        csa = normalize_string(row.get('csa', ''))
        rx_otc = normalize_string(row.get('rx_otc', ''))

        canon_key = get_canonical_medicine_key(drug_name)
        med_id = canonical_med_map.get(canon_key)
        
        if not med_id:
            search_tokens = f"{drug_name} {generic_name} {canon_key}".lower()
            cursor.execute("""
                INSERT INTO medicines (canonical_name, brand_name, generic_name, canonical_key, search_tokens, pregnancy_category, csa_schedule, rx_otc, type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'allopathy');
            """, (drug_name, drug_name, generic_name, canon_key, search_tokens, preg_cat, csa, rx_otc))
            med_id = cursor.lastrowid
            canonical_med_map[canon_key] = med_id
            raw_name_to_id[drug_name.lower()] = med_id
        else:
            cursor.execute("""
                UPDATE medicines 
                SET generic_name = COALESCE(generic_name, ?),
                    pregnancy_category = COALESCE(pregnancy_category, ?),
                    csa_schedule = COALESCE(csa_schedule, ?),
                    rx_otc = COALESCE(rx_otc, ?)
                WHERE id = ?;
            """, (generic_name, preg_cat, csa, rx_otc, med_id))

        cond = normalize_string(row.get('medical_condition', ''))
        if cond: uses_records.append((med_id, cond))

        se_text = normalize_string(row.get('side_effects', ''))
        if se_text: side_effects_records.append((med_id, se_text[:250], 'Common'))

    cursor.executemany("INSERT INTO medicine_ingredients (medicine_id, ingredient_name, strength, unit) VALUES (?, ?, ?, ?);", ingredients_to_insert)
    cursor.executemany("INSERT INTO medicine_aliases (medicine_id, alias_name) VALUES (?, ?);", aliases_to_insert)
    cursor.executemany("INSERT INTO substitutes (medicine_id, substitute_name, substitute_medicine_id) VALUES (?, ?, ?);", substitutes_records)
    cursor.executemany("INSERT INTO side_effects (medicine_id, side_effect_name, frequency) VALUES (?, ?, ?);", side_effects_records)
    cursor.executemany("INSERT INTO medicine_uses (medicine_id, use_name) VALUES (?, ?);", uses_records)
    conn.commit()

    print(f"  Inserted {len(ingredients_to_insert)} ingredients, {len(aliases_to_insert)} aliases, {len(substitutes_records)} substitutes, {len(side_effects_records)} side effects.")

    # -------------------------------------------------------------
    # [Step 4/7] Process Diseases & Symptoms (With Metadata & Severity)
    # -------------------------------------------------------------
    print("\n[Step 4/7] Processing Diseases & Severity Classifications...")

    symptom_severity_data = read_csv('Symptom-severity.csv')
    symptom_records = []
    for row in symptom_severity_data:
        sym_name = clean_symptom_name(row.get('Symptom', ''))
        weight = int(row.get('weight', 1))
        if sym_name: symptom_records.append((sym_name, weight))

    cursor.executemany("INSERT OR IGNORE INTO symptoms (name, severity_weight) VALUES (?, ?);", symptom_records)
    conn.commit()

    desc_data = read_csv('description.csv')
    disease_desc_map = {clean_disease_name(row.get('Disease', '')): normalize_string(row.get('Description', '')) for row in desc_data if row.get('Disease')}

    all_disease_names = set(disease_desc_map.keys())
    for fname in ['Symptom2Disease.csv', 'symtoms_df.csv', 'diets.csv', 'workout_df.csv']:
        for row in read_csv(fname):
            d_name = clean_disease_name(row.get('label') or row.get('Disease') or row.get('disease') or '')
            if d_name: all_disease_names.add(d_name)

    for d_name in sorted(all_disease_names):
        desc = disease_desc_map.get(d_name, '')
        sev = DISEASE_SEVERITIES.get(d_name, 'Moderate')
        cursor.execute("INSERT OR IGNORE INTO diseases (name, severity_level, description) VALUES (?, ?, ?);", (d_name, sev, desc))
    conn.commit()

    cursor.execute("SELECT name, id FROM diseases;")
    for d_n, d_id in cursor.fetchall():
        diseases_map[d_n] = d_id

    # -------------------------------------------------------------
    # [Step 5/7] Link Disease Relationships (Symptoms, Precautions, Diets, Workouts)
    # -------------------------------------------------------------
    print("\n[Step 5/7] Linking Reverse Symptom & Disease Relations...")

    ds_records = set()
    for row in read_csv('symtoms_df.csv'):
        d_name = clean_disease_name(row.get('Disease', ''))
        d_id = diseases_map.get(d_name)
        if not d_id: continue
        
        for i in range(1, 5):
            sym_name = clean_symptom_name(row.get(f'Symptom_{i}', ''))
            if sym_name:
                cursor.execute("INSERT OR IGNORE INTO symptoms (name, severity_weight) VALUES (?, 1);", (sym_name,))
                cursor.execute("SELECT id FROM symptoms WHERE name = ?;", (sym_name,))
                sym_id = cursor.fetchone()[0]
                symptoms_map[sym_name] = sym_id
                ds_records.add((d_id, sym_id))

    training_filepath = os.path.join(RAW_DATA_DIR, 'Training.csv')
    if os.path.exists(training_filepath):
        with open(training_filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            symptom_cols = headers[:-1]
            
            for row in reader:
                if not row: continue
                prognosis = clean_disease_name(row[-1])
                d_id = diseases_map.get(prognosis)
                if not d_id: continue
                
                for idx, val in enumerate(row[:-1]):
                    if val == '1':
                        sym_name = clean_symptom_name(symptom_cols[idx])
                        cursor.execute("INSERT OR IGNORE INTO symptoms (name, severity_weight) VALUES (?, 1);", (sym_name,))
                        cursor.execute("SELECT id FROM symptoms WHERE name = ?;", (sym_name,))
                        sym_id = cursor.fetchone()[0]
                        symptoms_map[sym_name] = sym_id
                        ds_records.add((d_id, sym_id))

    cursor.executemany("INSERT OR IGNORE INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?);", list(ds_records))

    # Precautions, Diets, Workouts
    prec_records = [(diseases_map[clean_disease_name(r['Disease'])], normalize_string(r[f'Precaution_{i}'])) 
                    for r in read_csv('precautions_df.csv') if clean_disease_name(r.get('Disease')) in diseases_map 
                    for i in range(1, 5) if normalize_string(r.get(f'Precaution_{i}'))]
    cursor.executemany("INSERT INTO disease_precautions (disease_id, precaution) VALUES (?, ?);", prec_records)

    diets_records = [(diseases_map[clean_disease_name(r['Disease'])], diet_item)
                     for r in read_csv('diets.csv') if clean_disease_name(r.get('Disease')) in diseases_map
                     for diet_item in parse_list_str(r.get('Diet', ''))]
    cursor.executemany("INSERT INTO disease_diets (disease_id, diet) VALUES (?, ?);", diets_records)

    workout_records = [(diseases_map[clean_disease_name(r['disease'])], normalize_string(r['workout']))
                       for r in read_csv('workout_df.csv') if clean_disease_name(r.get('disease')) in diseases_map and normalize_string(r.get('workout'))]
    cursor.executemany("INSERT INTO disease_workouts (disease_id, workout) VALUES (?, ?);", workout_records)
    conn.commit()

    # -------------------------------------------------------------
    # [Step 6/7] Drug Interactions with Severity Tags
    # -------------------------------------------------------------
    print("\n[Step 6/7] Processing Drug Interactions & Severity Classification...")
    interactions_data = read_csv('db_drug_interactions.csv')

    interaction_records = []
    for row in interactions_data:
        d1 = normalize_string(row.get('Drug 1', ''))
        d2 = normalize_string(row.get('Drug 2', ''))
        desc = normalize_string(row.get('Interaction Description', ''))
        
        if not d1 or not d2 or not desc: continue

        d1_ckey = get_canonical_medicine_key(d1)
        d2_ckey = get_canonical_medicine_key(d2)

        d1_id = canonical_med_map.get(d1_ckey)
        d2_id = canonical_med_map.get(d2_ckey)

        sev, sev_tag = classify_interaction_severity(desc)
        interaction_records.append((d1, d2, d1_id, d2_id, sev, sev_tag, desc))

    cursor.executemany("""
        INSERT INTO drug_interactions (drug_a_name, drug_b_name, drug_a_id, drug_b_id, severity, severity_tag, interaction_description)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, interaction_records)
    conn.commit()

    # Indexes
    cursor.executescript("""
        CREATE INDEX idx_medicines_canon_name ON medicines(canonical_name);
        CREATE INDEX idx_medicines_canon_key ON medicines(canonical_key);
        CREATE INDEX idx_medicines_mfg ON medicines(manufacturer_id);
        CREATE INDEX idx_ingredients_med ON medicine_ingredients(medicine_id);
        CREATE INDEX idx_ingredients_name ON medicine_ingredients(ingredient_name);
        CREATE INDEX idx_aliases_med ON medicine_aliases(medicine_id);
        CREATE INDEX idx_synonyms_src ON synonyms(source_term);
        CREATE INDEX idx_diseases_name ON diseases(name);
        CREATE INDEX idx_symptoms_name ON symptoms(name);
        CREATE INDEX idx_drug_interactions_ab ON drug_interactions(drug_a_name, drug_b_name);
        CREATE INDEX idx_side_effects_med ON side_effects(medicine_id);
        CREATE INDEX idx_medicine_uses_med ON medicine_uses(medicine_id);
        CREATE INDEX idx_substitutes_med ON substitutes(medicine_id);
    """)
    conn.commit()

    # -------------------------------------------------------------
    # [Step 7/7] PostgreSQL Dump Script Export
    # -------------------------------------------------------------
    print("\n[Step 7/7] Exporting PostgreSQL Dump Script (medical_db_dump.sql)...")
    
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    with open(POSTGRES_DUMP, 'w', encoding='utf-8') as f:
        f.write("-- PostgreSQL Export File for Medical Database\n")
        f.write("-- Generated automatically by Phase 1.1 - 1.12 Data Engineering ETL\n\n")
        f.write(schema_sql)
        f.write("\n\n-- DATA INSERTIONS --\n\n")

        def dump_table(table_name, columns):
            cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name};")
            rows = cursor.fetchall()
            if not rows: return
            
            f.write(f"\n-- Inserts for {table_name} ({len(rows)} records)\n")
            batch_size = 500
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i+batch_size]
                val_strs = []
                for row in batch:
                    formatted_vals = []
                    for v in row:
                        if v is None:
                            formatted_vals.append("NULL")
                        elif isinstance(v, (int, float)):
                            formatted_vals.append(str(v))
                        else:
                            clean_str = str(v).replace("'", "''")
                            formatted_vals.append(f"'{clean_str}'")
                    val_strs.append(f"({', '.join(formatted_vals)})")
                
                insert_stmt = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n" + ",\n".join(val_strs) + ";\n"
                f.write(insert_stmt)

        dump_table("manufacturers", ["id", "name"])
        dump_table("medicines", ["id", "canonical_name", "brand_name", "generic_name", "canonical_key", "search_tokens", "price_inr", "is_discontinued", "pack_size_label", "composition", "type", "pregnancy_category", "alcohol_warning", "csa_schedule", "rx_otc", "manufacturer_id"])
        dump_table("medicine_ingredients", ["id", "medicine_id", "ingredient_name", "strength", "unit"])
        dump_table("medicine_aliases", ["id", "medicine_id", "alias_name"])
        dump_table("synonyms", ["id", "source_term", "canonical_term", "category"])
        dump_table("diseases", ["id", "name", "severity_level", "description", "causes", "risk_factors", "complications", "diagnosis", "treatment"])
        dump_table("symptoms", ["id", "name", "severity_weight"])
        dump_table("disease_symptoms", ["disease_id", "symptom_id"])
        dump_table("disease_precautions", ["disease_id", "precaution"])
        dump_table("disease_diets", ["disease_id", "diet"])
        dump_table("disease_workouts", ["disease_id", "workout"])
        dump_table("drug_interactions", ["id", "drug_a_name", "drug_b_name", "drug_a_id", "drug_b_id", "severity", "severity_tag", "interaction_description"])
        dump_table("side_effects", ["id", "medicine_id", "side_effect_name", "frequency"])
        dump_table("medicine_uses", ["id", "medicine_id", "use_name"])
        dump_table("substitutes", ["id", "medicine_id", "substitute_name", "substitute_medicine_id"])

    conn.close()

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 65)
    print(f"Phase 1.1 - 1.12 ETL Pipeline Successfully Completed in {elapsed}s!")
    print(f"SQLite DB Created: {OUTPUT_DB}")
    print(f"PostgreSQL SQL Dump Created: {POSTGRES_DUMP}")
    print("=" * 65)

if __name__ == '__main__':
    run_etl()
