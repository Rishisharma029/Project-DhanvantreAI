import sqlite3

def verify():
    conn = sqlite3.connect('medical_database.db')
    c = conn.cursor()
    tables = [
        'manufacturers', 'medicines', 'diseases', 'symptoms',
        'disease_symptoms', 'disease_precautions', 'disease_diets',
        'disease_workouts', 'drug_interactions', 'side_effects',
        'medicine_uses', 'substitutes'
    ]

    print("=" * 55)
    print("      DATABASE RECORD COUNTS & VERIFICATION")
    print("=" * 55)
    for t in tables:
        c.execute(f"SELECT COUNT(*) FROM {t};")
        cnt = c.fetchone()[0]
        print(f"  {t:<22}: {cnt:>10,}")

    print("\n" + "=" * 55)
    print("               DATABASE INDEXES")
    print("=" * 55)
    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
    for name, tbl in c.fetchall():
        print(f"  Index: {name:<28} on table: {tbl}")

    print("\n" + "=" * 55)
    print("         SAMPLE DATA CHECK (MEDICINE)")
    print("=" * 55)
    c.execute("""
        SELECT m.id, m.raw_name, m.normalized_name, m.price_inr, m.composition, mfg.name 
        FROM medicines m 
        LEFT JOIN manufacturers mfg ON m.manufacturer_id = mfg.id 
        WHERE m.normalized_name LIKE '%augmentin%' LIMIT 3;
    """)
    for row in c.fetchall():
        print(" ", row)

    conn.close()

if __name__ == '__main__':
    verify()
