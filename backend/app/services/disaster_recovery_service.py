import os
import time
import glob
import sqlite3
import base64
import hashlib
from typing import Dict, Any, List
from cryptography.fernet import Fernet
from app.config import settings

def _derive_fernet_key(secret_key: str) -> bytes:
    """Derive a URL-safe base64-encoded 32-byte key for Fernet AES-256 encryption."""
    hashed = hashlib.sha256(secret_key.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(hashed)

class DisasterRecoveryEngine:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = os.path.abspath(backup_dir)
        os.makedirs(self.backup_dir, exist_ok=True)
        self.fernet_key = _derive_fernet_key(settings.SECRET_KEY)
        self.cipher = Fernet(self.fernet_key)

    def create_encrypted_backup(self, db_path: str = "medical_database.db") -> Dict[str, Any]:
        """Creates an AES-256 encrypted snapshot of the database."""
        abs_db_path = os.path.abspath(db_path)
        if not os.path.exists(abs_db_path):
            raise FileNotFoundError(f"Database file not found at path: {abs_db_path}")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_filename = f"auramed_backup_{timestamp}.enc.db"
        encrypted_backup_path = os.path.join(self.backup_dir, backup_filename)

        with open(abs_db_path, "rb") as f_in:
            raw_db_bytes = f_in.read()

        encrypted_bytes = self.cipher.encrypt(raw_db_bytes)

        with open(encrypted_backup_path, "wb") as f_out:
            f_out.write(encrypted_bytes)

        checksum = hashlib.sha256(raw_db_bytes).hexdigest()

        return {
            "status": "success",
            "backup_filename": backup_filename,
            "backup_path": encrypted_backup_path,
            "original_size_bytes": len(raw_db_bytes),
            "encrypted_size_bytes": len(encrypted_bytes),
            "sha256_checksum": checksum,
            "timestamp": timestamp
        }

    def restore_and_verify_backup(self, encrypted_backup_path: str, temp_verify_dir: str = "backups/temp_verify") -> Dict[str, Any]:
        """
        Decrypts backup file and performs restore schema & integrity verification.
        """
        abs_backup_path = os.path.abspath(encrypted_backup_path)
        if not os.path.exists(abs_backup_path):
            raise FileNotFoundError(f"Encrypted backup file not found at: {abs_backup_path}")

        os.makedirs(temp_verify_dir, exist_ok=True)
        restored_test_db = os.path.join(temp_verify_dir, f"restored_verify_{int(time.time())}.db")

        try:
            with open(abs_backup_path, "rb") as f_in:
                encrypted_bytes = f_in.read()

            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)

            with open(restored_test_db, "wb") as f_out:
                f_out.write(decrypted_bytes)

            # Perform Integrity Query Verification
            conn = sqlite3.connect(restored_test_db)
            cursor = conn.cursor()
            cursor.execute("PRAGMA quick_check;")
            integrity_res = cursor.fetchone()[0]

            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table';")
            table_count = cursor.fetchone()[0]

            conn.close()

            is_valid = (integrity_res == "ok" and table_count > 0)
            checksum = hashlib.sha256(decrypted_bytes).hexdigest()

            return {
                "restore_status": "verified" if is_valid else "corrupted",
                "integrity_check": integrity_res,
                "table_count": table_count,
                "decrypted_size_bytes": len(decrypted_bytes),
                "sha256_checksum": checksum,
                "is_valid": is_valid
            }
        finally:
            if os.path.exists(restored_test_db):
                try:
                    os.remove(restored_test_db)
                except Exception:
                    pass

    def list_backups(self) -> List[Dict[str, Any]]:
        """Lists available encrypted backups with file metadata."""
        pattern = os.path.join(self.backup_dir, "*.enc.db")
        backup_files = glob.glob(pattern)
        results = []

        for b_path in sorted(backup_files, reverse=True):
            stat = os.stat(b_path)
            results.append({
                "filename": os.path.basename(b_path),
                "path": b_path,
                "size_bytes": stat.st_size,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(stat.st_ctime))
            })

        return results

# Singleton Disaster Recovery Instance
disaster_recovery_engine = DisasterRecoveryEngine()
