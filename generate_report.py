import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

def generate_report(db_path='medical_database.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    def get_cnt(query):
        c.execute(query)
        return c.fetchone()[0]

    med_cnt = get_cnt("SELECT COUNT(*) FROM medicines;")
    alias_cnt = get_cnt("SELECT COUNT(*) FROM medicine_aliases;")
    ing_cnt = get_cnt("SELECT COUNT(*) FROM medicine_ingredients;")
    mfg_cnt = get_cnt("SELECT COUNT(*) FROM manufacturers;")
    inter_cnt = get_cnt("SELECT COUNT(*) FROM drug_interactions;")
    sub_cnt = get_cnt("SELECT COUNT(*) FROM substitutes;")
    se_cnt = get_cnt("SELECT COUNT(*) FROM side_effects;")
    use_cnt = get_cnt("SELECT COUNT(*) FROM medicine_uses;")
    dis_cnt = get_cnt("SELECT COUNT(*) FROM diseases;")
    sym_cnt = get_cnt("SELECT COUNT(*) FROM symptoms;")
    prec_cnt = get_cnt("SELECT COUNT(*) FROM disease_precautions;")
    diet_cnt = get_cnt("SELECT COUNT(*) FROM disease_diets;")
    work_cnt = get_cnt("SELECT COUNT(*) FROM disease_workouts;")
    syn_cnt = get_cnt("SELECT COUNT(*) FROM synonyms;")

    c.execute("SELECT severity_tag, COUNT(*) FROM drug_interactions GROUP BY severity_tag;")
    inter_sev = c.fetchall()

    c.execute("SELECT severity_level, COUNT(*) FROM diseases GROUP BY severity_level;")
    dis_sev = c.fetchall()

    print("=" * 65)
    print("        MEDICAL PLATFORM — DATASET STATISTICS REPORT")
    print("=" * 65)
    print(f"  Master Canonical Medicines : {med_cnt:>12,}")
    print(f"  Brand Variants / Aliases   : {alias_cnt:>12,}")
    print(f"  Parsed Ingredients         : {ing_cnt:>12,}")
    print(f"  Pharmaceutical Mfgs        : {mfg_cnt:>12,}")
    print(f"  Drug-Drug Interactions     : {inter_cnt:>12,}")
    print(f"  Medicine Substitutes       : {sub_cnt:>12,}")
    print(f"  Side Effects               : {se_cnt:>12,}")
    print(f"  Therapeutic Uses           : {use_cnt:>12,}")
    print(f"  Diseases                   : {dis_cnt:>12,}")
    print(f"  Symptoms                   : {sym_cnt:>12,}")
    print(f"  Disease Precautions        : {prec_cnt:>12,}")
    print(f"  Diet Recommendations       : {diet_cnt:>12,}")
    print(f"  Workout Plans              : {work_cnt:>12,}")
    print(f"  Medical Synonyms           : {syn_cnt:>12,}")

    print("\n" + "-" * 65)
    print("  DRUG INTERACTION SEVERITY BREAKDOWN:")
    for tag, cnt in inter_sev:
        print(f"    - {tag:<18}: {cnt:>10,}")

    print("\n" + "-" * 65)
    print("  DISEASE SEVERITY LEVEL BREAKDOWN:")
    for level, cnt in dis_sev:
        print(f"    - {level:<18}: {cnt:>10,}")
    print("=" * 65)

    conn.close()

if __name__ == '__main__':
    generate_report()
