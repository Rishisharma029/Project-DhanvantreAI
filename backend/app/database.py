import sqlite3
import os
from app.config import settings

def _ensure_valid_sqlite_db(db_path: str):
    """If db_path is an un-fetched Git LFS pointer text file or invalid header, remove it so sqlite3 initializes a fresh valid database."""
    if os.path.exists(db_path):
        try:
            with open(db_path, "rb") as f:
                header = f.read(16)
                if header.startswith(b"version https://") or (len(header) > 0 and not header.startswith(b"SQLite format 3")):
                    f.close()
                    os.remove(db_path)
        except Exception:
            pass

def get_db():
    """
    Dependency that provides a database connection.
    Closes the connection after request is completed.
    """
    db_path = settings.DATABASE_PATH
    _ensure_valid_sqlite_db(db_path)
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 30000;")
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()

def init_user_db():
    """Ensure user-related tables exist in the medical database."""
    _ensure_valid_sqlite_db(settings.DATABASE_PATH)
    conn = sqlite3.connect(settings.DATABASE_PATH, timeout=30.0)
    conn.execute("PRAGMA busy_timeout = 30000;")
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'user', -- user, doctor, admin
            is_active INTEGER DEFAULT 1,
            is_verified INTEGER DEFAULT 0,
            password_changed_at TIMESTAMP DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS refresh_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            revoked INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS auth_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            token_type TEXT NOT NULL, -- email_verify, password_reset
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS revoked_jwt_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jti TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            reason TEXT DEFAULT 'logout', -- logout, password_reset, compromised_account
            revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS ai_feedback_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            feedback_type TEXT NOT NULL, -- RATING, INCORRECT_SUGGESTION, MISSING_DATA, PROMPT_OPTIMIZATION
            rating INTEGER,
            query_or_context TEXT,
            ai_response TEXT,
            user_comment TEXT,
            reported_category TEXT, -- MISDIAGNOSIS, WRONG_DOSAGE, MISSING_DRUG, MISSING_SYMPTOM, OTHER
            suggested_correction TEXT,
            status TEXT DEFAULT 'PENDING_REVIEW', -- PENDING_REVIEW, RESOLVED, PROMPT_OPTIMIZED, RETRIEVAL_INDEXED
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
        );



        CREATE TABLE IF NOT EXISTS user_medical_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            age INTEGER,
            gender TEXT, -- Male, Female, Other, Prefer not to say
            height_cm REAL,
            weight_kg REAL,
            bmi REAL,
            blood_group TEXT, -- A+, A-, B+, B-, AB+, AB-, O+, O-
            pregnancy_status INTEGER DEFAULT 0,
            allergies TEXT DEFAULT '[]', -- JSON array
            chronic_diseases TEXT DEFAULT '[]', -- JSON array
            current_medications TEXT DEFAULT '[]', -- JSON array
            past_medical_history TEXT,
            family_history TEXT,
            smoking_status TEXT DEFAULT 'Non-Smoker', -- Non-Smoker, Occasional, Regular, Former
            alcohol_consumption TEXT DEFAULT 'None', -- None, Occasional, Moderate, Heavy
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_uuid TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            title TEXT DEFAULT 'New Consultation',
            is_active INTEGER DEFAULT 1,
            last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            sender TEXT NOT NULL, -- user, assistant, system
            content TEXT NOT NULL,
            metadata TEXT DEFAULT '{}', -- JSON for citations or confidence scores
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
        );

        -- Module 2.19 Medical History Service Tables
        CREATE TABLE IF NOT EXISTS user_medical_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            report_type TEXT NOT NULL, -- Blood Test, Lab Report, Imaging, Clinical Notes
            report_date TEXT NOT NULL,
            summary_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS user_symptom_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symptom_name TEXT NOT NULL,
            severity TEXT DEFAULT 'Moderate', -- Mild, Moderate, Severe
            onset_date TEXT NOT NULL,
            resolution_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS user_medication_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            side_effects_noted TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS user_followup_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            reason TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0,
            clinical_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- Module 2.20 Notification Service Table
        CREATE TABLE IF NOT EXISTS user_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            notification_type TEXT NOT NULL, -- Password Reset, Report Ready, Follow-up Reminder, General Email
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            recipient_email TEXT NOT NULL,
            status TEXT DEFAULT 'SENT', -- PENDING, SENT, FAILED
            scheduled_for TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- Module 2.23 Analytics Engine Tables
        CREATE TABLE IF NOT EXISTS search_query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 0,
            query_text TEXT NOT NULL,
            domain TEXT DEFAULT 'all', -- medicines, diseases, symptoms, ingredients, manufacturers, all
            results_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ai_usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_id INTEGER DEFAULT 0,
            query_text TEXT NOT NULL,
            tools_called_count INTEGER DEFAULT 0,
            latency_ms INTEGER DEFAULT 0,
            is_emergency INTEGER DEFAULT 0,
            safety_score REAL DEFAULT 100.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Module 2.24 Logging & Audit Engine Tables
        CREATE TABLE IF NOT EXISTS system_audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 0,
            log_type TEXT NOT NULL, -- API_REQUEST, ERROR, AI_CALL, SEARCH_QUERY
            endpoint TEXT,
            method TEXT,
            status_code INTEGER,
            latency_ms INTEGER DEFAULT 0,
            message TEXT,
            details_json TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS recommendation_history_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 0,
            session_id TEXT,
            symptoms_json TEXT NOT NULL,
            disease_recommendations_json TEXT NOT NULL,
            medicine_recommendations_json TEXT DEFAULT '[]',
            safety_warnings_json TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

        -- Migration: Add password_changed_at column if not present
        PRAGMA table_info(users);
    """)

    # Ensure password_changed_at column exists
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users);")
    columns = [row[1] for row in cursor.fetchall()]
    if "password_changed_at" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_changed_at TIMESTAMP DEFAULT NULL;")

    # Ensure password_changed_at column exists in auth_tokens refresh check
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_refresh_token ON refresh_tokens(token);
        CREATE INDEX IF NOT EXISTS idx_auth_token ON auth_tokens(token);
        CREATE INDEX IF NOT EXISTS idx_profile_user_id ON user_medical_profiles(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON chat_sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_uuid ON chat_sessions(session_uuid);
        CREATE INDEX IF NOT EXISTS idx_messages_session_id ON chat_messages(session_id);
        CREATE INDEX IF NOT EXISTS idx_reports_user_id ON user_medical_reports(user_id);
        CREATE INDEX IF NOT EXISTS idx_symptom_hist_user_id ON user_symptom_history(user_id);
        CREATE INDEX IF NOT EXISTS idx_med_hist_user_id ON user_medication_history(user_id);
        CREATE INDEX IF NOT EXISTS idx_followup_user_id ON user_followup_visits(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON user_notifications(user_id);
        CREATE INDEX IF NOT EXISTS idx_search_logs_query ON search_query_logs(query_text);
        CREATE INDEX IF NOT EXISTS idx_ai_logs_user ON ai_usage_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_log_type ON system_audit_logs(log_type);
        CREATE INDEX IF NOT EXISTS idx_rec_hist_user ON recommendation_history_logs(user_id);
    """)

    # Seed Default Temporary / Demo Users
    try:
        from app.services.auth_service import hash_password
        hashed_demo_pwd = hash_password("Password123!")
        hashed_admin_pwd = hash_password("AdminPassword123!")

        cursor.execute("""
            INSERT OR IGNORE INTO users (id, email, hashed_password, full_name, role, is_active, is_verified)
            VALUES (1, 'demo@auramed.ai', ?, 'Demo Clinical User', 'user', 1, 1);
        """, (hashed_demo_pwd,))

        cursor.execute("""
            INSERT OR IGNORE INTO users (id, email, hashed_password, full_name, role, is_active, is_verified)
            VALUES (2, 'admin@auramed.ai', ?, 'System Administrator', 'admin', 1, 1);
        """, (hashed_admin_pwd,))
    except Exception as e:
        print(f"Warning: Demo user seeding skipped: {e}")

    conn.commit()
    conn.close()

