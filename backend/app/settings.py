from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "Shelter Capacity API"
    API_VERSION: str = "0.1.0"

    # Accepts either a real list in .env (e.g., ["http://localhost:5173","http://127.0.0.1:5173"])
    # or a comma-separated string (e.g., http://localhost:5173,http://127.0.0.1:5173)
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # -----------------------------
    # DB (use Postgres in prod; SQLite in dev is fine)
    # Example Postgres: postgresql+psycopg://user:pass@host:5432/db
    # -----------------------------
    DATABASE_URL: str = "sqlite:///./dev.db"


    # Auth (Marker 3)
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Email (SMTP)
    # Use Gmail App Password (NOT your real password) if using Gmail.
    EMAIL_ENABLED: bool = False
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_STARTTLS: bool = True
    SMTP_USER: str = ""          # e.g., youraddress@gmail.com
    SMTP_PASSWORD: str = ""      # app password if using Gmail
    EMAIL_FROM: str = ""         # e.g., "Shelter App <youraddress@gmail.com>"
    EMAIL_TO_DEFAULT: str = ""   # fallback recipient if shelter has no email yet

    # SMS (Twilio)
    TWILIO_ENABLED: bool = False
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_FROM_NUMBER: str = ""   # E164, e.g. "+18551234567", optional if using Messaging Service:
                                    # send_sms_twilio("Hello from Shelter App 🚀", to_number="+18777804236")
    TWILIO_MESSAGING_SERVICE_SID: str = ""   # optional alternative; e.g., "MGxxxxxxxx..."
                                    # send_sms_twilio("Using MSG Service SID", to_number="+18777804236", messaging_service_sid="MG7711b495ac20b5155b59b035b5a42f9e")

    TEST_SMS_TO: str = ""           # local testing convenience


    # Pydantic v2 config (do NOT add class Config)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore extra env vars instead of raising
    )

    # Normalize BACKEND_CORS_ORIGINS from .env:
    #  - if it's a JSON array string, parse it as JSON
    #  - otherwise, treat as comma-separated list
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def parse_cors(cls, v):
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                # JSON array
                import json
                try:
                    return json.loads(s)
                except Exception:
                    # fall back to comma split if malformed JSON
                    pass
            # comma-separated
            return [item.strip() for item in s.split(",") if item.strip()]
        return v

settings = Settings()
