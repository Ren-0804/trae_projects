from fastapi import APIRouter
from app.api.v1 import auth, drivers, statistics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["司机管理"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["统计"])