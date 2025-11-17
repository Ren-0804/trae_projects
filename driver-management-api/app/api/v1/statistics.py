from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, extract, and_, select
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.models import User, Driver, Vehicle, Schedule, DriverCertificate, MaintenanceRecord
from app.crud import get_drivers_count
from app.schemas import StatisticsResponse

router = APIRouter()


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取统计数据（管理员权限）"""
    
    # 司机总数
    total_drivers = await get_drivers_count(db)
    
    # 活跃司机数
    active_drivers = await get_drivers_count(db, status="active")
    
    # 本月新增司机数
    now = datetime.utcnow()
    first_day_of_month = datetime(now.year, now.month, 1)
    
    # 查询本月新增司机数
    new_drivers_this_month_query = await db.execute(
        select(func.count(Driver.id))
        .where(Driver.created_at >= first_day_of_month)
    )
    new_drivers_this_month = new_drivers_this_month_query.scalar()
    
    # 按线路统计
    drivers_by_route_query = await db.execute(
        select(
            Driver.main_route,
            func.count(Driver.id).label("count")
        ).group_by(Driver.main_route)
        .order_by(func.count(Driver.id).desc())
        .limit(10)
    )
    drivers_by_route = [
        {"route": row[0], "count": row[1]}
        for row in drivers_by_route_query.fetchall()
    ]
    
    # 按员工统计
    drivers_by_user_query = await db.execute(
        select(
            Driver.user_id,
            User.username,
            func.count(Driver.id).label("count")
        ).join(User, Driver.user_id == User.id)
        .group_by(Driver.user_id, User.username)
        .order_by(func.count(Driver.id).desc())
        .limit(10)
    )
    drivers_by_user = [
        {"user_id": row[0], "username": row[1], "count": row[2]}
        for row in drivers_by_user_query.fetchall()
    ]
    
    # 车辆统计
    total_vehicles_query = await db.execute(select(func.count(Vehicle.id)))
    total_vehicles = total_vehicles_query.scalar()
    
    active_vehicles_query = await db.execute(
        select(func.count(Vehicle.id)).where(Vehicle.status == "active")
    )
    active_vehicles = active_vehicles_query.scalar()
    
    # 排班统计
    total_schedules_query = await db.execute(select(func.count(Schedule.id)))
    total_schedules = total_schedules_query.scalar()
    
    completed_schedules_query = await db.execute(
        select(func.count(Schedule.id)).where(Schedule.status == "completed")
    )
    completed_schedules = completed_schedules_query.scalar()
    
    # 过期证书统计
    today = datetime.now().date()
    expired_certificates_query = await db.execute(
        select(func.count(DriverCertificate.id))
        .where(DriverCertificate.expiry_date < today)
        .where(DriverCertificate.status == "valid")
    )
    expired_certificates = expired_certificates_query.scalar()
    
    # 即将到期的维护统计
    future_date = today + timedelta(days=30)
    upcoming_maintenance_query = await db.execute(
        select(func.count(MaintenanceRecord.id))
        .where(MaintenanceRecord.next_service_date >= today)
        .where(MaintenanceRecord.next_service_date <= future_date)
        .where(MaintenanceRecord.status == "completed")
    )
    upcoming_maintenance = upcoming_maintenance_query.scalar()
    
    # 活跃紧急警报统计
    active_emergency_alerts_query = await db.execute(
        select(func.count(func.distinct(Driver.id)))
        .where(Driver.status == "active")
    )
    # 这里简化处理，实际需要查询紧急警报表
    active_emergency_alerts = 0  # 暂时设为0，后续实现紧急警报功能时再更新
    
    return {
        "total_drivers": total_drivers,
        "active_drivers": active_drivers,
        "new_drivers_this_month": new_drivers_this_month,
        "drivers_by_route": drivers_by_route,
        "drivers_by_user": drivers_by_user,
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "total_schedules": total_schedules,
        "completed_schedules": completed_schedules,
        "expired_certificates": expired_certificates,
        "upcoming_maintenance": upcoming_maintenance,
        "active_emergency_alerts": active_emergency_alerts
    }


@router.get("/dashboard")
async def get_dashboard_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取仪表板统计数据"""
    
    # 获取今日统计数据
    today = datetime.utcnow().date()
    
    # 今日排班数
    today_schedules_query = await db.execute(
        select(func.count(Schedule.id))
        .where(Schedule.schedule_date >= datetime.combine(today, datetime.min.time()))
        .where(Schedule.schedule_date < datetime.combine(today + timedelta(days=1), datetime.min.time()))
    )
    today_schedules = today_schedules_query.scalar()
    
    # 今日完成排班数
    today_completed_query = await db.execute(
        select(func.count(Schedule.id))
        .where(Schedule.schedule_date >= datetime.combine(today, datetime.min.time()))
        .where(Schedule.schedule_date < datetime.combine(today + timedelta(days=1), datetime.min.time()))
        .where(Schedule.status == "completed")
    )
    today_completed = today_completed_query.scalar()
    
    # 即将到期的证书（7天内）
    expiring_certificates_query = await db.execute(
        select(func.count(DriverCertificate.id))
        .where(DriverCertificate.expiry_date >= today)
        .where(DriverCertificate.expiry_date <= today + timedelta(days=7))
        .where(DriverCertificate.status == "valid")
    )
    expiring_certificates = expiring_certificates_query.scalar()
    
    # 即将到期的维护（7天内）
    upcoming_maintenance_query = await db.execute(
        select(func.count(Vehicle.id))
        .where(Vehicle.maintenance_due_date >= today)
        .where(Vehicle.maintenance_due_date <= today + timedelta(days=7))
        .where(Vehicle.status == "active")
    )
    upcoming_maintenance = upcoming_maintenance_query.scalar()
    
    return {
        "today_schedules": today_schedules,
        "today_completed_schedules": today_completed,
        "expiring_certificates_7days": expiring_certificates,
        "upcoming_maintenance_7days": upcoming_maintenance,
        "active_drivers": await get_drivers_count(db, status="active"),
        "active_vehicles": await db.execute(select(func.count(Vehicle.id)).where(Vehicle.status == "active")).scalar()
    }