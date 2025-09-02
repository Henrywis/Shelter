from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

# For SQLite, echo=False to reduce noise; for Postgres, keep pool_pre_ping
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
