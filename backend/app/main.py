from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .api import runs, history, auth

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="SoundCloud Weekly Updater",
    description="Web interface for SoundCloud automation scripts",
    version="1.0.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(runs.router, prefix="/api/runs", tags=["runs"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "SoundCloud Weekly Updater"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SoundCloud Weekly Updater API",
        "docs": "/docs",
        "health": "/api/health"
    }
