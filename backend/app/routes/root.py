from fastapi import APIRouter
from ..settings import settings
from ..db import ping_db

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"project": settings.PROJECT_NAME, "api_version": settings.API_VERSION}

@router.get("/db-check")
def db_check():
    return {"database": "up" if ping_db() else "down"}
