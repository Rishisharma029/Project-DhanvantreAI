import os
import sys
import tempfile
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.database_backup_service import (
    create_encrypted_database_backup, restore_encrypted_database_backup
)


def test_encrypted_database_backup_and_restore():
    """Test AES-256 encrypted database snapshot creation and integrity restoration."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db = os.path.join(tmp_dir, "test_medical.db")
        backup_dir = os.path.join(tmp_dir, "backups")
        restored_db = os.path.join(tmp_dir, "restored_medical.db")

        # 1. Create a dummy SQLite database with patient record
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE patient_records (id INTEGER PRIMARY KEY, note TEXT);")
        cursor.execute("INSERT INTO patient_records (note) VALUES ('Sample confidential note');")
        conn.commit()
        conn.close()

        # 2. Perform AES-256 Encrypted Backup
        passphrase = "super-secret-healthcare-encryption-key-2026"
        res = create_encrypted_database_backup(db_path=test_db, backup_dir=backup_dir, passphrase=passphrase)
        assert res["status"] == "success"
        backup_path = res["backup_path"]
        assert os.path.exists(backup_path)

        # Ensure raw file content does NOT contain plaintext database strings
        with open(backup_path, "rb") as f:
            encrypted_content = f.read()
        assert b"Sample confidential note" not in encrypted_content
        assert b"patient_records" not in encrypted_content

        # 3. Restore Encrypted Backup and Verify Integrity
        is_valid = restore_encrypted_database_backup(backup_filepath=backup_path, target_db_path=restored_db, passphrase=passphrase)
        assert is_valid is True

        # Query restored database
        conn_res = sqlite3.connect(restored_db)
        cur_res = conn_res.cursor()
        cur_res.execute("SELECT note FROM patient_records WHERE id = 1;")
        row = cur_res.fetchone()
        conn_res.close()

        assert row is not None
        assert row[0] == "Sample confidential note"

def test_encrypted_backup_invalid_passphrase():
    """Test that decryption fails cleanly when supplied with an invalid passphrase."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db = os.path.join(tmp_dir, "test_medical.db")
        backup_dir = os.path.join(tmp_dir, "backups")
        restored_db = os.path.join(tmp_dir, "restored_medical.db")

        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INT);")
        conn.commit()
        conn.close()

        res = create_encrypted_database_backup(db_path=test_db, backup_dir=backup_dir, passphrase="correct-key")
        backup_path = res["backup_path"]

        with pytest.raises(ValueError):
            restore_encrypted_database_backup(backup_filepath=backup_path, target_db_path=restored_db, passphrase="wrong-key")
