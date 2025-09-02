from fastapi import APIRouter
from ..settings import settings

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {
        "project": settings.PROJECT_NAME,
        "api_version": settings.API_VERSION
    }
