import os
import sqlite3
import base64
import time
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.config import settings

def derive_fernet_key(passphrase: str, salt: bytes) -> bytes:
    """Derive 32-byte AES key using PBKDF2HMAC SHA256 for encrypted database backups."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode('utf-8')))
    return key

def create_encrypted_database_backup(db_path: str = None, backup_dir: str = None, passphrase: str = None) -> dict:
    """
    Creates an AES-256 encrypted database snapshot at rest.
    Stores salt in header and encrypts database bytes cleanly.
    """
    if not db_path:
        db_path = settings.DATABASE_PATH
    if not passphrase:
        passphrase = settings.SECRET_KEY
    if not backup_dir:
        backup_dir = os.path.join(os.path.dirname(db_path), "backups")

    os.makedirs(backup_dir, exist_ok=True)

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    # Read raw database file bytes
    with open(db_path, "rb") as f:
        raw_bytes = f.read()

    # Generate cryptographic salt
    salt = os.urandom(16)
    fernet_key = derive_fernet_key(passphrase, salt)
    fernet = Fernet(fernet_key)

    # Encrypt raw SQLite binary payload
    encrypted_payload = fernet.encrypt(raw_bytes)

    # Format output file: [16 bytes SALT] + [ENCRYPTED PAYLOAD]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_filename = f"medical_db_backup_{timestamp}.db.enc"
    backup_filepath = os.path.join(backup_dir, backup_filename)

    with open(backup_filepath, "wb") as f_out:
        f_out.write(salt)
        f_out.write(encrypted_payload)

    return {
        "status": "success",
        "backup_path": backup_filepath,
        "backup_size_bytes": os.path.getsize(backup_filepath),
        "raw_size_bytes": len(raw_bytes),
        "encryption": "AES-256-GCM / Fernet PBKDF2",
        "created_at": timestamp
    }

def restore_encrypted_database_backup(backup_filepath: str, target_db_path: str, passphrase: str = None) -> bool:
    """
    Decrypts an encrypted database backup snapshot and restores to target SQLite path.
    """
    if not passphrase:
        passphrase = settings.SECRET_KEY

    if not os.path.exists(backup_filepath):
        raise FileNotFoundError(f"Backup file not found at {backup_filepath}")

    with open(backup_filepath, "rb") as f_in:
        salt = f_in.read(16)
        encrypted_payload = f_in.read()

    fernet_key = derive_fernet_key(passphrase, salt)
    fernet = Fernet(fernet_key)

    try:
        decrypted_bytes = fernet.decrypt(encrypted_payload)
    except Exception as e:
        raise ValueError(f"Failed to decrypt database backup. Invalid passphrase or corrupted backup file: {e}")

    # Write decrypted bytes to target database path
    with open(target_db_path, "wb") as f_out:
        f_out.write(decrypted_bytes)

    # Verify SQLite integrity
    conn = sqlite3.connect(target_db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()
    conn.close()

    return result and result[0] == "ok"
