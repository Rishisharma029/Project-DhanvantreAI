import sqlite3
import os

db_path = 'medical_database.db'
dump_path = 'medical_db_dump.sql'

print("Removing corrupted DB...")
if os.path.exists(db_path):
    os.remove(db_path)

print("Restoring from dump...")
conn = sqlite3.connect(db_path)
with open(dump_path, 'r', encoding='utf-8') as f:
    conn.executescript(f.read())
conn.close()
print("Restore complete.")
