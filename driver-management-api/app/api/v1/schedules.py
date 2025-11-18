from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User
from app.schemas import ScheduleCreate, ScheduleUpdate, ScheduleResponse

router = APIRouter()


@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    driver_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    schedule_date: Optional[date] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None, pattern="^(scheduled|in_progress|completed|cancelled)$"),
    task_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取排班列表 - 简化版本"""
    logger.info(f"用户 {current_user.username} 请求排班列表")
    return []  # 返回空列表作为临时解决方案


@router.post("/", response_model=ScheduleResponse)
async def create_schedule(
    schedule: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建排班 - 简化版本"""
    logger.info(f"用户 {current_user.username} 尝试创建排班")
    # 返回一个模拟的响应
    return ScheduleResponse(
        id=1,
        driver_id=schedule.driver_id,
        vehicle_id=schedule.vehicle_id,
        schedule_date=schedule.schedule_date,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        route=schedule.route,
        task_type=schedule.task_type,
        status="scheduled",
        notes=schedule.notes,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取排班详情 - 简化版本"""
    logger.info(f"用户 {current_user.username} 请求排班详情 ID: {schedule_id}")
    raise HTTPException(status_code=404, detail="排班不存在")