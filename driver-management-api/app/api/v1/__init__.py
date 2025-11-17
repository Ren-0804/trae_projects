from fastapi import APIRouter
from app.api.v1 import auth, drivers, statistics, regions, vehicles, schedules, certificates, safety, reminders

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["司机管理"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["车辆管理"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["排班管理"])
api_router.include_router(certificates.router, prefix="/certificates", tags=["证书管理"])
api_router.include_router(safety.router, prefix="/safety", tags=["安全管理"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["统计"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["提醒管理"])
api_router.include_router(regions.router, prefix="", tags=["地区信息"])