from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    # 数据库配置 - 使用SQLite简化开发
    DATABASE_URL: str = "sqlite+aiosqlite:///./driver_management.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    ALGORITHM: str = "HS256"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"]
    
    # 文件上传配置
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # 管理员配置
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "admin123"
    DEFAULT_ADMIN_PASSWORD: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 创建上传目录
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)