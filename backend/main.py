from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.api.router import router

# Load environment variables
load_dotenv()

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

# Include API router
app.include_router(router)

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
    gemini_key_set = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "gemini_api_key_configured": gemini_key_set
    }

