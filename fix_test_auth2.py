"""Fix test_auth.py line that expects reset_token in response"""

filepath = r"backend\tests\test_auth.py"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and replace the line
for i, line in enumerate(lines):
    if 'forgot_res.json()["reset_token"]' in line:
        lines[i] = '''    # Token is not returned in response for security - fetch from DB for testing
    import sqlite3
    import os
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "medical_database.db")
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT token FROM auth_tokens WHERE token_type = 'password_reset' ORDER BY id DESC LIMIT 1;")
    reset_token = cursor.fetchone()["token"]
    db.close()
'''
        print(f"Fixed line {i+1}")
        break

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Done")
