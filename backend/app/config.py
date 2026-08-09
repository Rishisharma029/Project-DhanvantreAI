import os

class Settings:
    PROJECT_NAME: str = "Medical Platform Intelligence API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-medical-platform-key-change-in-production-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24

    # Database
    ROOT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", os.path.join(ROOT_DIR, "medical_database.db"))

    # Environment & Security
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    ENFORCE_HTTPS: bool = os.getenv("ENFORCE_HTTPS", "false").lower() == "true"
    CORS_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,https://auramed.ai"
        ).split(",") if origin.strip()
    ]

settings = Settings()



