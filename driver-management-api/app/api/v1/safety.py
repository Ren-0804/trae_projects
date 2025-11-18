from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User
from app.schemas import (
    GPSRecordCreate, GPSRecordResponse,
    DrivingBehaviorCreate, DrivingBehaviorUpdate, DrivingBehaviorResponse,
    EmergencyAlertCreate, EmergencyAlertUpdate, EmergencyAlertResponse
)

router = APIRouter()


@router.get("/stats")
async def get_safety_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取安全统计（仪表板期望字段）"""
    logger.info(f"用户 {current_user.username} 请求安全统计")
    return {
        "online_drivers": 0,
        "active_vehicles": 0,
        "today_alerts": 0,
        "emergency_alerts": 0
    }


@router.get("/alerts/recent")
async def get_recent_alerts(
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取最近预警 - 简化版本，返回 data 包装"""
    logger.info(f"用户 {current_user.username} 请求最近预警，限制: {limit}")
    return {"data": []}


@router.post("/gps-records", response_model=GPSRecordResponse)
async def create_gps_record(
    gps_record: GPSRecordCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建GPS记录 - 简化版本"""
    logger.info(f"用户 {current_user.username} 尝试创建GPS记录")
    return GPSRecordResponse(
        id=1,
        vehicle_id=gps_record.vehicle_id,
        driver_id=gps_record.driver_id,
        latitude=gps_record.latitude,
        longitude=gps_record.longitude,
        speed=gps_record.speed,
        direction=gps_record.direction,
        altitude=gps_record.altitude,
        timestamp=gps_record.timestamp or datetime.now(),
        created_at=datetime.now()
    )


@router.get("/gps-records", response_model=List[GPSRecordResponse])
async def get_gps_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vehicle_id: Optional[int] = Query(None),
    driver_id: Optional[int] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取GPS记录列表 - 简化版本"""
    logger.info(f"用户 {current_user.username} 请求GPS记录列表")
    return []


@router.post("/driving-behaviors", response_model=DrivingBehaviorResponse)
async def create_driving_behavior(
    behavior: DrivingBehaviorCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建驾驶行为记录 - 简化版本"""
    logger.info(f"用户 {current_user.username} 尝试创建驾驶行为记录")
    return DrivingBehaviorResponse(
        id=1,
        driver_id=behavior.driver_id,
        vehicle_id=behavior.vehicle_id,
        behavior_type=behavior.behavior_type,
        severity=behavior.severity,
        description=behavior.description,
        location=behavior.location,
        latitude=behavior.latitude,
        longitude=behavior.longitude,
        recorded_at=behavior.recorded_at or datetime.now(),
        created_at=datetime.now()
    )


@router.get("/driving-behaviors", response_model=List[DrivingBehaviorResponse])
async def get_driving_behaviors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    driver_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    behavior_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取驾驶行为记录列表 - 简化版本"""
    logger.info(f"用户 {current_user.username} 请求驾驶行为记录列表")
    return []


@router.post("/emergency-alerts", response_model=EmergencyAlertResponse)
async def create_emergency_alert(
    alert: EmergencyAlertCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建紧急预警 - 简化版本"""
    logger.info(f"用户 {current_user.username} 尝试创建紧急预警")
    return EmergencyAlertResponse(
        id=1,
        alert_type=alert.alert_type,
        severity=alert.severity,
        title=alert.title,
        description=alert.description,
        driver_id=alert.driver_id,
        vehicle_id=alert.vehicle_id,
        location=alert.location,
        latitude=alert.latitude,
        longitude=alert.longitude,
        status="active",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@router.get("/emergency-alerts", response_model=List[EmergencyAlertResponse])
async def get_emergency_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, pattern="^(active|resolved|ignored)$"),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    driver_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取紧急预警列表 - 简化版本"""
    logger.info(f"用户 {current_user.username} 请求紧急预警列表")
    return []


@router.put("/emergency-alerts/{alert_id}", response_model=EmergencyAlertResponse)
async def update_emergency_alert(
    alert_id: int,
    alert_update: EmergencyAlertUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新紧急预警 - 简化版本"""
    logger.info(f"用户 {current_user.username} 尝试更新紧急预警 {alert_id}")
    return EmergencyAlertResponse(
        id=alert_id,
        alert_type="sos",
        severity="high",
        title="测试预警",
        description="这是一个测试预警",
        status=alert_update.status or "resolved",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )