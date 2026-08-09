import os
import sys
import tempfile
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.database_backup_service import (
    create_encrypted_database_backup, restore_encrypted_database_backup
)
from app.config import settings

def run_backup_restore_testing():
    print("[+] Starting Automated Backup & Restore Verification Test...")

    db_path = settings.DATABASE_PATH
    if not os.path.exists(db_path):
        print(f"[-] Error: Database path {db_path} does not exist.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp_dir:
        backup_dir = os.path.join(tmp_dir, "backups")
        restored_db_path = os.path.join(tmp_dir, "restored_medical_test.db")

        # Step 1: Create AES-256 Encrypted Backup Snapshot
        print("  1. Creating Versioned AES-256 Encrypted Database Backup...")
        backup_res = create_encrypted_database_backup(db_path=db_path, backup_dir=backup_dir)
        backup_file = backup_res["backup_path"]
        print(f"     [SUCCESS] Backup Created: {os.path.basename(backup_file)} ({backup_res['backup_size_bytes']} bytes)")

        # Step 2: Attempt Decryption & Restoration
        print("  2. Testing Decryption & Database Restoration...")
        is_integrity_valid = restore_encrypted_database_backup(backup_filepath=backup_file, target_db_path=restored_db_path)
        print(f"     [SUCCESS] Decryption Restored cleanly to temporary target.")

        # Step 3: Verify Integrity & Row Counts
        print("  3. Verifying Database PRAGMA Integrity & Record Counts...")
        conn_orig = sqlite3.connect(db_path)
        conn_rest = sqlite3.connect(restored_db_path)

        cur_orig = conn_orig.cursor()
        cur_rest = conn_rest.cursor()

        cur_orig.execute("SELECT COUNT(*) FROM medicines;")
        orig_meds = cur_orig.fetchone()[0]

        cur_rest.execute("SELECT COUNT(*) FROM medicines;")
        rest_meds = cur_rest.fetchone()[0]

        cur_rest.execute("PRAGMA integrity_check;")
        integrity = cur_rest.fetchone()[0]

        conn_orig.close()
        conn_rest.close()

        print(f"     * Original Medicines Count : {orig_meds}")
        print(f"     * Restored Medicines Count : {rest_meds}")
        print(f"     * Database Integrity Check : {integrity.upper()}")

        assert orig_meds == rest_meds, "Mismatch in restored row count!"
        assert integrity == "ok", "Database integrity check failed!"

        print("[SUCCESS] ALL BACKUP & RESTORE INTEGRITY VERIFICATIONS PASSED 100%!")

if __name__ == "__main__":
    run_backup_restore_testing()
