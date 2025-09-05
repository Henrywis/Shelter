from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import root
from .routes import auth as auth_routes
from .routes import capacity as capacity_routes
from .routes import intake as intake_routes
from .routes import shelters as shelters_routes
from .settings import settings


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
app.include_router(auth_routes.router)
app.include_router(capacity_routes.router)
app.include_router(intake_routes.router)
app.include_router(shelters_routes.router)

# Future:
# from .routes import shelters, capacity, intake
# app.include_router(shelters.router, prefix="/shelters", tags=["shelters"])... Done
# app.include_router(capacity.router, prefix="/capacity", tags=["capacity"])...Done
# app.include_router(intake.router, prefix="/intake", tags=["intake"])...Now
