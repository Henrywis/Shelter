from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .settings import settings

# For SQLite, echo=False to reduce noise; for Postgres, keep pool_pre_ping
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ping_db() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False