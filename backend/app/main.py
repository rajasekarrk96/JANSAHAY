from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import auth, services, cases, documents, ai, notifications, admin
from app.db.session import AsyncSessionLocal
from app.db.init_db import init_db_data
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JANSAHAY: Citizen-First Public-Service Journey & Secure Government Workflow Engine"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(services.router, prefix=settings.API_V1_STR)
app.include_router(cases.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
async def on_startup():
    # Ensure storage paths
    os.makedirs(settings.STORAGE_PATH, exist_ok=True)
    # Initialize DB if jansahay.db is absent
    if "sqlite" in settings.DATABASE_URL:
        db_file = settings.DATABASE_URL.replace("sqlite+aiosqlite:///", "")
        if not os.path.exists(db_file):
            async with AsyncSessionLocal() as session:
                await init_db_data(session)

@app.get("/")
async def root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "platform": "JANSAHAY",
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "documentation": "/docs",
        "compliance": "Hackathon Prototype - 100% Synthetic Data & Sandboxed Execution"
    }
