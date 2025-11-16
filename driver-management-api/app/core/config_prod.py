import os
from typing import List, Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./driver_management.db"
    
    # Redis Configuration (Optional)
    REDIS_URL: Optional[str] = None
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://traetraeprojectshsqb.vercel.app"]
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "pdf"]
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Security Settings
    BCRYPT_ROUNDS: int = 12
    CSRF_SECRET_KEY: str = "your-csrf-secret-key-change-in-production"
    
    # Production Settings
    DEBUG: bool = False
    RELOAD: bool = False
    WORKERS: int = 4
    
    class Config:
        env_file = ".env.prod"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Production environment detection
if not settings.DEBUG:
    # Ensure secret keys are changed in production
    if settings.SECRET_KEY == "your-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must be changed in production!")
    if settings.JWT_SECRET_KEY == "your-jwt-secret-key-change-in-production":
        raise ValueError("JWT_SECRET_KEY must be changed in production!")
    if settings.CSRF_SECRET_KEY == "your-csrf-secret-key-change-in-production":
        raise ValueError("CSRF_SECRET_KEY must be changed in production!")