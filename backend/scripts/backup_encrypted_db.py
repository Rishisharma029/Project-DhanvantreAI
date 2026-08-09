import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.database_backup_service import create_encrypted_database_backup

def main():
    print("[+] Initiating Healthcare Database Encryption & Snapshot Backup...")
    res = create_encrypted_database_backup()
    print("[SUCCESS] Encrypted Database Snapshot Created Successfully!")
    print(f"   * Destination Path  : {res['backup_path']}")
    print(f"   * Backup Size       : {res['backup_size_bytes']} bytes")
    print(f"   * Encryption Format : {res['encryption']}")
    print(f"   * Timestamp         : {res['created_at']}")


if __name__ == "__main__":
    main()
