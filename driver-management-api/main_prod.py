"""
Production-ready Driver Management System API
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import logging
import os
from contextlib import asynccontextmanager

from app.api.v1 import auth, drivers, statistics, users
from app.core.database import engine, Base
from app.core.config_prod import settings
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Driver Management System API...")
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created/updated")
    logger.info(f"Application started with {settings.WORKERS} workers")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Driver Management System API...")
    await engine.dispose()

# Create FastAPI app
app = FastAPI(
    title="Driver Management System API",
    description="Production-ready API for driver management system",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1", "traetraeprojectshsqb.vercel.app"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Static files for uploads
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 50001,
            "message": "Internal server error",
            "data": {"detail": "An unexpected error occurred"},
            "timestamp": int(os.times().system)
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": int(os.times().system)
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Driver Management System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(drivers.router, prefix="/api/v1/drivers", tags=["Drivers"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["Statistics"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server with {settings.WORKERS} workers...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        workers=settings.WORKERS,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )