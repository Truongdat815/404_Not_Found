from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from dotenv import load_dotenv
from app.api.router import router
from app.api.history_router import router as history_router
from app.api.export_router import router as export_router
from app.database.db import init_db, get_engine
from app.utils.logger import logger

# Load environment variables
load_dotenv()

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.warning(f"Database initialization warning: {str(e)}")
    logger.warning("Server will continue, but history features may not work")

app = FastAPI(
    title="AI Requirements Engineering API",
    description="API for analyzing SRS and User Stories using AI (Gemini)",
    version="1.0.0"
)

# CORS middleware để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(router)
app.include_router(history_router)
app.include_router(export_router)

@app.get("/")
async def root():
    return {
        "message": "AI Requirements Engineering API",
        "status": "running",
        "docs": "/docs",
        "ai_provider": "Google Gemini"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint - kiểm tra status của API, Gemini, và Database"""
    gemini_key_set = bool(os.getenv("GEMINI_API_KEY"))
    
    # Check database connection
    db_status = "unknown"
    try:
        engine = get_engine()
        if engine:
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            db_status = "connected"
        else:
            db_status = "not_configured"
    except Exception as e:
        db_status = f"error: {str(e)[:50]}"
        logger.warning(f"Database health check failed: {str(e)}")
    
    status = "healthy" if gemini_key_set and db_status == "connected" else "degraded"
    
    return {
        "status": status,
        "api": "running",
        "gemini_api_key_configured": gemini_key_set,
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    }

