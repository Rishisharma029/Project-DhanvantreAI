import sqlite3
import json
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.config import settings
from app.data.disease_kb import DISEASE_KB

def sync_kb_to_db():
    sys.stdout.reconfigure(encoding='utf-8')
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    print("TABLES:")
    for row in cursor.fetchall():
        print(row[0])
        
    # Let's count diseases
    cursor.execute("SELECT COUNT(*) FROM diseases")
    count = cursor.fetchone()[0]
    print(f"\nDiseases in DB: {count}")
    
    # We will insert missing diseases.
    # The schema for diseases is: id, name, severity_level, description
    # The schema for symptoms is: id, name
    # The schema for disease_symptoms is: disease_id, symptom_id
    
    # Prepare to insert
    new_diseases = 0
    for name, data in DISEASE_KB.items():
        cursor.execute("SELECT id FROM diseases WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            # Insert disease
            cursor.execute("INSERT INTO diseases (name, severity_level, description) VALUES (?, ?, ?)", 
                           (name, data.get("severity", "Moderate"), data.get("icd11", "")))
            disease_id = cursor.lastrowid
            new_diseases += 1
        else:
            disease_id = row[0]
            
        # Insert symptoms
        for sym in data.get("symptoms", []):
            sym_clean = sym.strip().lower()
            cursor.execute("SELECT id FROM symptoms WHERE name = ?", (sym_clean,))
            s_row = cursor.fetchone()
            if not s_row:
                cursor.execute("INSERT INTO symptoms (name) VALUES (?)", (sym_clean,))
                sym_id = cursor.lastrowid
            else:
                sym_id = s_row[0]
                
            # Link
            cursor.execute("SELECT 1 FROM disease_symptoms WHERE disease_id = ? AND symptom_id = ?", (disease_id, sym_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?)", (disease_id, sym_id))
                
    conn.commit()
    print(f"Added {new_diseases} new diseases to the DB.")
    
    # Count again
    cursor.execute("SELECT COUNT(*) FROM diseases")
    count = cursor.fetchone()[0]
    print(f"Total diseases now: {count}")
    
    conn.close()

if __name__ == '__main__':
    sync_kb_to_db()
