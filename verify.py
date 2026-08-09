import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

def verify_database(db_path='medical_database.db'):
    print("=" * 65)
    print("      AUTOMATED DATA QUALITY VALIDATION SUITE (verify.py)")
    print("=" * 65)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    errors_found = 0

    # Test 1: Missing values (empty medicine names)
    c.execute("SELECT COUNT(*) FROM medicines WHERE canonical_name IS NULL OR TRIM(canonical_name) = '';")
    empty_meds = c.fetchone()[0]
    status1 = "PASS" if empty_meds == 0 else f"FAIL ({empty_meds} empty names)"
    print(f" 1. Missing Essential Values Check : [ {status1} ]")
    if empty_meds > 0: errors_found += 1

    # Test 2: Broken Foreign Keys
    c.execute("PRAGMA foreign_key_check;")
    fk_errors = c.fetchall()
    status2 = "PASS (0 broken FKs)" if len(fk_errors) == 0 else f"FAIL ({len(fk_errors)} broken FKs)"
    print(f" 2. Foreign Key Integrity Check    : [ {status2} ]")
    if len(fk_errors) > 0: errors_found += 1

    # Test 3: Duplicate Primary Keys
    c.execute("SELECT id, COUNT(*) FROM medicines GROUP BY id HAVING COUNT(*) > 1;")
    dup_ids = c.fetchall()
    status3 = "PASS (0 duplicate IDs)" if len(dup_ids) == 0 else f"FAIL ({len(dup_ids)} duplicate IDs)"
    print(f" 3. Unique Primary Key Audit       : [ {status3} ]")
    if len(dup_ids) > 0: errors_found += 1

    # Test 4: Empty Descriptions (Diseases)
    c.execute("SELECT COUNT(*) FROM diseases WHERE description IS NULL OR TRIM(description) = '';")
    empty_desc = c.fetchone()[0]
    status4 = f"PASS ({empty_desc} missing descriptions)" if empty_desc < 10 else f"WARNING ({empty_desc} missing)"
    print(f" 4. Disease Description Coverage   : [ {status4} ]")

    # Test 5: Orphan Medicines (No uses, side effects, or ingredients)
    c.execute("""
        SELECT COUNT(*) FROM medicines m
        WHERE NOT EXISTS (SELECT 1 FROM medicine_ingredients i WHERE i.medicine_id = m.id)
          AND NOT EXISTS (SELECT 1 FROM medicine_uses u WHERE u.medicine_id = m.id)
          AND NOT EXISTS (SELECT 1 FROM side_effects s WHERE s.medicine_id = m.id);
    """)
    orphan_meds = c.fetchone()[0]
    status5 = "PASS" if orphan_meds == 0 else f"INFO ({orphan_meds:,} standalone medicines)"
    print(f" 5. Standalone / Orphan Meds Check : [ {status5} ]")

    # Test 6: Invalid Prices (< 0)
    c.execute("SELECT COUNT(*) FROM medicines WHERE price_inr < 0;")
    invalid_prices = c.fetchone()[0]
    status6 = "PASS (0 negative prices)" if invalid_prices == 0 else f"FAIL ({invalid_prices} invalid prices)"
    print(f" 6. Price Value Validity           : [ {status6} ]")
    if invalid_prices > 0: errors_found += 1

    # Test 7: Invalid Interactions (missing drug names)
    c.execute("SELECT COUNT(*) FROM drug_interactions WHERE drug_a_name IS NULL OR drug_b_name IS NULL OR TRIM(drug_a_name) = '' OR TRIM(drug_b_name) = '';")
    invalid_interactions = c.fetchone()[0]
    status7 = "PASS" if invalid_interactions == 0 else f"FAIL ({invalid_interactions} invalid interactions)"
    print(f" 7. Drug Interaction Quality       : [ {status7} ]")
    if invalid_interactions > 0: errors_found += 1

    print("-" * 65)
    if errors_found == 0:
        print("RESULT: ALL CRITICAL DATA VALIDATION CHECKS PASSED SUCCESSFULLY!")
    else:
        print(f"RESULT: {errors_found} VALIDATION CHECKS FAILED.")

    conn.close()

if __name__ == '__main__':
    verify_database()
