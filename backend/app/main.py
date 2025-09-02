from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .routes import root

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(root.router, prefix="")

# Future:
# from .routes import shelters, capacity, intake
# app.include_router(shelters.router, prefix="/shelters", tags=["shelters"])
# app.include_router(capacity.router, prefix="/capacity", tags=["capacity"])
# app.include_router(intake.router, prefix="/intake", tags=["intake"])
