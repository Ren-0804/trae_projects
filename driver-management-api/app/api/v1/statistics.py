from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, extract, and_, select

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.models import User, Driver
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
    from datetime import datetime, timedelta
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
    
    return {
        "total_drivers": total_drivers,
        "active_drivers": active_drivers,
        "new_drivers_this_month": new_drivers_this_month,
        "drivers_by_route": drivers_by_route,
        "drivers_by_user": drivers_by_user
    }