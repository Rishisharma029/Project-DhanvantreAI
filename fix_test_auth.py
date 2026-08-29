"""Update test_auth.py to work with the new security behavior"""

filepath = r"backend\tests\test_auth.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# The forgot-password endpoint no longer returns the reset_token
# (security: don't leak tokens). The test needs to fetch the token from the DB.
old_test = '''def test_password_reset_flow():
    client.post("/api/v1/auth/register", json={"email": "resetuser@med.org", "password": "oldPassword123", "full_name": "Reset User"})

    # Request reset token
    forgot_res = client.post("/api/v1/auth/forgot-password", json={"email": "resetuser@med.org"})
    assert forgot_res.status_code == 200
    reset_token = forgot_res.json()["reset_token"]'''

new_test = '''def test_password_reset_flow():
    import sqlite3
    import os
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "medical_database.db")
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    
    client.post("/api/v1/auth/register", json={"email": "resetuser@med.org", "password": "oldPassword123", "full_name": "Reset User"})

    # Request reset token
    forgot_res = client.post("/api/v1/auth/forgot-password", json={"email": "resetuser@med.org"})
    assert forgot_res.status_code == 200
    # Token is not returned in response for security - fetch from DB for testing
    cursor.execute("SELECT token FROM auth_tokens WHERE token_type = 'password_reset' ORDER BY id DESC LIMIT 1;")
    reset_token = cursor.fetchone()["token"]
    db.close()'''

content = content.replace(old_test, new_test)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("test_auth.py updated")
