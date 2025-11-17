from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User, Schedule, Driver, Vehicle
from app.schemas import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.crud import create_operation_log

router = APIRouter(prefix="/schedules", tags=["schedules"])


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
    db: Session = Depends(get_db)
):
    """获取排班列表"""
    try:
        query = db.query(Schedule)
        
        if driver_id:
            query = query.filter(Schedule.driver_id == driver_id)
        if vehicle_id:
            query = query.filter(Schedule.vehicle_id == vehicle_id)
        if schedule_date:
            query = query.filter(
                Schedule.schedule_date >= datetime.combine(schedule_date, datetime.min.time()),
                Schedule.schedule_date < datetime.combine(schedule_date + timedelta(days=1), datetime.min.time())
            )
        if start_date:
            query = query.filter(Schedule.schedule_date >= datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query = query.filter(Schedule.schedule_date < datetime.combine(end_date + timedelta(days=1), datetime.min.time()))
        if status:
            query = query.filter(Schedule.status == status)
        if task_type:
            query = query.filter(Schedule.task_type == task_type)
            
        schedules = query.order_by(Schedule.schedule_date.desc(), Schedule.start_time.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"用户 {current_user.username} 获取了 {len(schedules)} 条排班记录")
        return schedules
        
    except Exception as e:
        logger.error(f"获取排班列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取排班列表失败")


@router.post("/", response_model=ScheduleResponse)
async def create_schedule(
    schedule: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建排班"""
    try:
        # 验证司机是否存在
        driver = db.query(Driver).filter(Driver.id == schedule.driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        # 验证车辆是否存在（如果指定了车辆）
        if schedule.vehicle_id:
            vehicle = db.query(Vehicle).filter(Vehicle.id == schedule.vehicle_id).first()
            if not vehicle:
                raise HTTPException(status_code=404, detail="车辆不存在")
                
        # 检查时间冲突
        conflicting_schedules = db.query(Schedule).filter(
            Schedule.driver_id == schedule.driver_id,
            Schedule.status.in_(["scheduled", "in_progress"]),
            Schedule.schedule_date == schedule.schedule_date,
            Schedule.start_time < schedule.end_time,
            Schedule.end_time > schedule.start_time
        ).all()
        
        if conflicting_schedules:
            raise HTTPException(status_code=400, detail="该时间段已有排班冲突")
        
        db_schedule = Schedule(**schedule.dict())
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="create",
            table_name="schedules",
            record_id=db_schedule.id,
            old_data=None,
            new_data=schedule.json()
        )
        
        logger.info(f"用户 {current_user.username} 为司机 {driver.name} 创建了排班")
        return db_schedule
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建排班失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建排班失败")


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取排班详情"""
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="排班不存在")
            
        logger.info(f"用户 {current_user.username} 查看了排班 {schedule_id}")
        return schedule
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取排班详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取排班详情失败")


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新排班"""
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="排班不存在")
            
        # 验证司机是否存在（如果更新司机）
        if schedule_update.driver_id:
            driver = db.query(Driver).filter(Driver.id == schedule_update.driver_id).first()
            if not driver:
                raise HTTPException(status_code=404, detail="司机不存在")
                
        # 验证车辆是否存在（如果更新车辆）
        if schedule_update.vehicle_id:
            vehicle = db.query(Vehicle).filter(Vehicle.id == schedule_update.vehicle_id).first()
            if not vehicle:
                raise HTTPException(status_code=404, detail="车辆不存在")
                
        # 检查时间冲突（如果更新时间）
        if schedule_update.start_time or schedule_update.end_time or schedule_update.schedule_date:
            start_time = schedule_update.start_time or schedule.start_time
            end_time = schedule_update.end_time or schedule.end_time
            schedule_date = schedule_update.schedule_date or schedule.schedule_date
            driver_id = schedule_update.driver_id or schedule.driver_id
            
            conflicting_schedules = db.query(Schedule).filter(
                Schedule.driver_id == driver_id,
                Schedule.status.in_(["scheduled", "in_progress"]),
                Schedule.id != schedule_id,
                Schedule.schedule_date == schedule_date,
                Schedule.start_time < end_time,
                Schedule.end_time > start_time
            ).all()
            
            if conflicting_schedules:
                raise HTTPException(status_code=400, detail="该时间段已有排班冲突")
        
        # 记录旧数据
        old_data = schedule.json()
        
        # 更新字段
        update_data = schedule_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(schedule, field, value)
            
        schedule.updated_at = datetime.now()
        db.commit()
        db.refresh(schedule)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="update",
            table_name="schedules",
            record_id=schedule_id,
            old_data=old_data,
            new_data=schedule.json()
        )
        
        logger.info(f"用户 {current_user.username} 更新了排班 {schedule_id}")
        return schedule
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新排班失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新排班失败")


@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除排班"""
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="排班不存在")
            
        # 记录排班信息用于日志
        schedule_data = schedule.json()
        
        db.delete(schedule)
        db.commit()
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="delete",
            table_name="schedules",
            record_id=schedule_id,
            old_data=schedule_data,
            new_data=None
        )
        
        logger.info(f"用户 {current_user.username} 删除了排班 {schedule_id}")
        return {"message": "排班删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除排班失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除排班失败")


@router.get("/calendar/{year}/{month}")
async def get_schedule_calendar(
    year: int,
    month: int,
    driver_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取月度排班日历"""
    try:
        # 验证年月
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="无效的月份")
            
        # 获取月份的第一天和最后一天
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
            
        query = db.query(Schedule).filter(
            Schedule.schedule_date >= first_day,
            Schedule.schedule_date <= last_day
        )
        
        if driver_id:
            query = query.filter(Schedule.driver_id == driver_id)
            
        schedules = query.order_by(Schedule.schedule_date, Schedule.start_time).all()
        
        # 按日期分组
        calendar_data = {}
        for schedule in schedules:
            date_str = schedule.schedule_date.strftime("%Y-%m-%d")
            if date_str not in calendar_data:
                calendar_data[date_str] = []
            calendar_data[date_str].append({
                "id": schedule.id,
                "driver_id": schedule.driver_id,
                "driver_name": schedule.driver.name if schedule.driver else None,
                "vehicle_id": schedule.vehicle_id,
                "vehicle_plate": schedule.vehicle.plate_number if schedule.vehicle else None,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "route": schedule.route,
                "task_type": schedule.task_type,
                "status": schedule.status,
                "notes": schedule.notes
            })
        
        logger.info(f"用户 {current_user.username} 获取了 {year}年{month}月的排班日历")
        return calendar_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取排班日历失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取排班日历失败")


@router.get("/conflicts/check")
async def check_schedule_conflicts(
    driver_id: int = Query(...),
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    schedule_date: date = Query(...),
    exclude_schedule_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """检查排班冲突"""
    try:
        if start_time >= end_time:
            raise HTTPException(status_code=400, detail="结束时间必须晚于开始时间")
            
        query = db.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.status.in_(["scheduled", "in_progress"]),
            Schedule.schedule_date == datetime.combine(schedule_date, datetime.min.time()),
            Schedule.start_time < end_time,
            Schedule.end_time > start_time
        )
        
        if exclude_schedule_id:
            query = query.filter(Schedule.id != exclude_schedule_id)
            
        conflicts = query.all()
        
        result = []
        for conflict in conflicts:
            result.append({
                "id": conflict.id,
                "driver_id": conflict.driver_id,
                "vehicle_id": conflict.vehicle_id,
                "start_time": conflict.start_time,
                "end_time": conflict.end_time,
                "route": conflict.route,
                "task_type": conflict.task_type,
                "status": conflict.status
            })
        
        logger.info(f"用户 {current_user.username} 检查了司机 {driver_id} 的排班冲突，发现 {len(result)} 个冲突")
        return {
            "has_conflicts": len(result) > 0,
            "conflicts": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"检查排班冲突失败: {str(e)}")
        raise HTTPException(status_code=500, detail="检查排班冲突失败")


@router.get("/drivers/{driver_id}/availability")
async def get_driver_availability(
    driver_id: int,
    date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取司机某天的可用时间段"""
    try:
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        # 获取当天的所有排班
        schedules = db.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.schedule_date == datetime.combine(date, datetime.min.time()),
            Schedule.status.in_(["scheduled", "in_progress"])
        ).order_by(Schedule.start_time).all()
        
        # 生成可用时间段（假设工作时间为 06:00-22:00）
        work_start = datetime.combine(date, datetime.min.time().replace(hour=6, minute=0))
        work_end = datetime.combine(date, datetime.min.time().replace(hour=22, minute=0))
        
        available_slots = []
        current_time = work_start
        
        for schedule in schedules:
            if current_time < schedule.start_time:
                available_slots.append({
                    "start_time": current_time,
                    "end_time": schedule.start_time,
                    "duration_minutes": int((schedule.start_time - current_time).total_seconds() / 60)
                })
            current_time = max(current_time, schedule.end_time)
        
        if current_time < work_end:
            available_slots.append({
                "start_time": current_time,
                "end_time": work_end,
                "duration_minutes": int((work_end - current_time).total_seconds() / 60)
            })
        
        logger.info(f"用户 {current_user.username} 获取了司机 {driver.name} 在 {date} 的可用时间段")
        return {
            "driver_id": driver_id,
            "driver_name": driver.name,
            "date": date,
            "available_slots": available_slots,
            "total_available_minutes": sum(slot["duration_minutes"] for slot in available_slots)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取司机可用时间失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取司机可用时间失败")