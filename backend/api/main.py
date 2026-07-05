"""
=========================================================
AI Lecture Assistant
FastAPI Application
=========================================================

Main Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.schema.upload import router as upload_router
from backend.api.schema.summary import router as summary_router
from backend.api.schema.notes import router as notes_router
from backend.api.schema.quiz import router as quiz_router
from backend.api.schema.chat import router as chat_router
from backend.api.schema.metadata import router as metadata_router

from backend.api.exceptions import register_exception_handlers
from backend.api.middleware import LoggingMiddleware

# =========================================================
# FastAPI App
# =========================================================

app = FastAPI(

    title="AI Lecture Assistant API",

    description="Backend API for AI Lecture Assistant",

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc"

)

# =========================================================
# CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)
app.add_middleware(

    LoggingMiddleware

)

# =========================================================
# Exception Handlers
# =========================================================

register_exception_handlers(app)

# =========================================================
# Routers
# =========================================================

app.include_router(upload_router)

app.include_router(summary_router)

app.include_router(notes_router)

app.include_router(quiz_router)

app.include_router(chat_router)

app.include_router(metadata_router)

# =========================================================
# Root Endpoint
# =========================================================

@app.get(
    "/",
    tags=["Root"]
)
def home():

    return {

        "project": "AI Lecture Assistant",

        "version": "1.0.0",

        "status": "running"

    }

# =========================================================
# Health Check
# =========================================================

@app.get(
    "/health",
    tags=["Health"]
)
def health():

    return {

        "success": True,

        "message": "Server is healthy."

    }

# =========================================================
# Startup Event
# =========================================================

@app.on_event("startup")
def startup():

    print("=" * 70)

    print("AI Lecture Assistant API Started")

    print("Swagger Docs : http://127.0.0.1:8000/docs")

    print("=" * 70)

# =========================================================
# Shutdown Event
# =========================================================

@app.on_event("shutdown")
def shutdown():

    print("=" * 70)

    print("AI Lecture Assistant API Stopped")

    print("=" * 70)