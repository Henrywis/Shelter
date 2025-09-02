from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "Shelter Capacity API"
    API_VERSION: str = "0.1.0"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # DB: use Postgres in prod; SQLite in dev is fine
    DATABASE_URL: str = "sqlite:///./dev.db"  # e.g. "postgresql+psycopg2://user:pass@host:5432/db"

    # Auth (Marker 3)
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
