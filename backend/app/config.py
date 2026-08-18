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
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1  # 1 hour for password reset links
    PASSWORD_CHANGED_AT_COLUMN: str = "password_changed_at"

    # Database
    ROOT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", os.path.join(ROOT_DIR, "medical_database.db"))

    # Environment & Security
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    ENFORCE_HTTPS: bool = os.getenv("ENFORCE_HTTPS", "false").lower() == "true"

    # Upload Type Whitelist
    ALLOWED_IMAGE_MIME_TYPES: list[str] = [
        "image/jpeg", "image/jpg", "image/png", "image/webp",
        "image/heic", "image/heif", "image/tiff", "image/bmp", "image/gif",
    ]
    ALLOWED_IMAGE_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".tiff", ".bmp", ".gif"]
    ALLOWED_DOCUMENT_MIME_TYPES: list[str] = [
        "application/pdf", "image/jpeg", "image/png", "image/tiff",
    ]
    ALLOWED_AUDIO_MIME_TYPES: list[str] = [
        "audio/wav", "audio/mpeg", "audio/mp3", "audio/webm", "audio/ogg",
        "audio/flac", "audio/aac",
    ]
    CORS_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,https://auramed.ai"
        ).split(",") if origin.strip()
    ]

    # Stripe / Payment Settings
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")

    # Server-Side Plan Catalog
    # Prices are in smallest currency unit (cents/paise). NEVER trust client-provided prices.
    # The subscription endpoint always looks up prices from this catalog.
    PLAN_CATALOG: dict[str, dict] = {
        "free": {
            "id": "free",
            "name": "Free Tier",
            "description": "Basic clinical decision support",
            "price_cents": 0,
            "currency": "usd",
            "stripe_price_id": "",  # Set via env or admin
            "features": ["basic_symptom_check", "5_queries_per_day"],
        },
        "pro": {
            "id": "pro",
            "name": "Pro Tier",
            "description": "Advanced clinical AI with full reasoning",
            "price_cents": 2999,  # $29.99/month
            "currency": "usd",
            "stripe_price_id": "",  # Set via env or admin
            "features": [
                "full_10_step_pipeline",
                "unlimited_queries",
                "document_ai",
                "voice_ai",
                "image_ai",
                "export_reports",
            ],
        },
        "enterprise": {
            "id": "enterprise",
            "name": "Enterprise Tier",
            "description": "Full platform access with API and support",
            "price_cents": 9999,  # $99.99/month
            "currency": "usd",
            "stripe_price_id": "",  # Set via env or admin
            "features": [
                "all_pro_features",
                "api_access",
                "priority_support",
                "custom_integrations",
                "audit_logs",
                "sla",
            ],
        },
    }

settings = Settings()



