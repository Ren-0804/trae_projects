from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, time
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User, Driver, Vehicle
from app.services.smart_scheduler import SmartSchedulerService

router = APIRouter(prefix="/schedules/smart", tags=["smart-scheduling"])

@router.post("/generate", response_model=dict)
async def generate_smart_schedule(
    schedule_date: datetime = Query(..., description="排班日期"),
    shift_start: str = Query(..., description="班次开始时间 (HH:MM)"),
    shift_end: str = Query(..., description="班次结束时间 (HH:MM)"),
    task_type: str = Query(..., pattern="^(delivery|pickup|transport)$", description="任务类型"),
    required_drivers: int = Query(1, ge=1, le=10, description="需要的司机数量"),
    prefer_experienced: bool = Query(False, description="优先选择经验丰富的司机"),
    prefer_high_rating: bool = Query(False, description="优先选择高评分司机"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成智能排班方案"""
    try:
        # 解析时间
        start_time = datetime.strptime(shift_start, "%H:%M").time()
        end_time = datetime.strptime(shift_end, "%H:%M").time()
        
        # 创建智能排班服务
        scheduler = SmartSchedulerService(db)
        
        # 偏好设置
        preferences = {
            'prefer_experienced': prefer_experienced,
            'prefer_high_rating': prefer_high_rating
        }
        
        # 生成最优方案
        schedules = scheduler.generate_optimal_schedule(
            schedule_date=schedule_date,
            shift_start=start_time,
            shift_end=end_time,
            task_type=task_type,
            required_drivers=required_drivers,
            preferences=preferences
        )
        
        logger.info(f"用户 {current_user.username} 生成智能排班方案成功，找到 {len(schedules)} 个方案")
        
        return {
            "success": True,
            "schedules": schedules,
            "total_options": len(schedules),
            "generation_time": datetime.now().isoformat()
        }
        
    except ValueError as e:
        logger.error(f"时间格式错误: {str(e)}")
        raise HTTPException(status_code=400, detail="时间格式错误，请使用 HH:MM 格式")
    except Exception as e:
        logger.error(f"生成智能排班方案失败: {str(e)}")
        raise HTTPException(status_code=500, detail="生成智能排班方案失败")


@router.post("/check-conflicts", response_model=dict)
async def check_schedule_conflicts(
    driver_id: int = Query(..., description="司机ID"),
    vehicle_id: int = Query(..., description="车辆ID"),
    schedule_date: datetime = Query(..., description="排班日期"),
    start_time: str = Query(..., description="开始时间 (HH:MM)"),
    end_time: str = Query(..., description="结束时间 (HH:MM)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """检查排班冲突"""
    try:
        # 解析时间
        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()
        
        # 创建智能排班服务
        scheduler = SmartSchedulerService(db)
        
        # 检查冲突
        conflicts = scheduler.check_schedule_conflicts(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            schedule_date=schedule_date,
            start_time=start_time_obj,
            end_time=end_time_obj
        )
        
        logger.info(f"用户 {current_user.username} 检查排班冲突成功")
        
        return {
            "success": True,
            "conflicts": conflicts,
            "can_schedule": not conflicts['has_conflict']
        }
        
    except ValueError as e:
        logger.error(f"时间格式错误: {str(e)}")
        raise HTTPException(status_code=400, detail="时间格式错误，请使用 HH:MM 格式")
    except Exception as e:
        logger.error(f"检查排班冲突失败: {str(e)}")
        raise HTTPException(status_code=500, detail="检查排班冲突失败")


@router.get("/driver-availability", response_model=dict)
async def get_driver_availability(
    schedule_date: datetime = Query(..., description="排班日期"),
    shift_start: str = Query(..., description="班次开始时间 (HH:MM)"),
    shift_end: str = Query(..., description="班次结束时间 (HH:MM)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取司机可用性"""
    try:
        # 解析时间
        start_time = datetime.strptime(shift_start, "%H:%M").time()
        end_time = datetime.strptime(shift_end, "%H:%M").time()
        
        # 创建智能排班服务
        scheduler = SmartSchedulerService(db)
        
        # 获取可用司机
        available_drivers = scheduler._get_available_drivers(schedule_date, start_time, end_time)
        
        # 构建响应数据
        driver_data = []
        for driver in available_drivers:
            # 获取司机最近的工作记录
            recent_schedules = scheduler._get_recent_driver_schedules(driver.id, 7)
            
            driver_info = {
                'id': driver.id,
                'name': driver.name,
                'phone': driver.phone,
                'license_number': driver.license_number,
                'experience_years': driver.experience_years,
                'safety_rating': driver.safety_rating,
                'recent_work_days': len(recent_schedules),
                'status': 'available'
            }
            driver_data.append(driver_info)
        
        logger.info(f"用户 {current_user.username} 获取司机可用性成功，找到 {len(driver_data)} 个可用司机")
        
        return {
            "success": True,
            "drivers": driver_data,
            "total_available": len(driver_data),
            "query_date": schedule_date.isoformat(),
            "shift_time": f"{shift_start} - {shift_end}"
        }
        
    except ValueError as e:
        logger.error(f"时间格式错误: {str(e)}")
        raise HTTPException(status_code=400, detail="时间格式错误，请使用 HH:MM 格式")
    except Exception as e:
        logger.error(f"获取司机可用性失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取司机可用性失败")


@router.get("/vehicle-availability", response_model=dict)
async def get_vehicle_availability(
    schedule_date: datetime = Query(..., description="排班日期"),
    shift_start: str = Query(..., description="班次开始时间 (HH:MM)"),
    shift_end: str = Query(..., description="班次结束时间 (HH:MM)"),
    task_type: Optional[str] = Query(None, pattern="^(delivery|pickup|transport)$", description="任务类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取车辆可用性"""
    try:
        # 解析时间
        start_time = datetime.strptime(shift_start, "%H:%M").time()
        end_time = datetime.strptime(shift_end, "%H:%M").time()
        
        # 创建智能排班服务
        scheduler = SmartSchedulerService(db)
        
        # 获取可用车辆
        available_vehicles = scheduler._get_available_vehicles(schedule_date, start_time, end_time)
        
        # 计算车辆评分
        vehicle_scores = scheduler._calculate_vehicle_scores(available_vehicles, task_type or 'transport')
        
        # 构建响应数据
        vehicle_data = []
        for vehicle_score in vehicle_scores:
            vehicle = vehicle_score['vehicle']
            
            vehicle_info = {
                'id': vehicle.id,
                'plate_number': vehicle.plate_number,
                'vehicle_type': vehicle.vehicle_type,
                'brand_model': vehicle.brand_model,
                'current_mileage': vehicle.current_mileage,
                'score': vehicle_score['score'],
                'status': 'available'
            }
            vehicle_data.append(vehicle_info)
        
        logger.info(f"用户 {current_user.username} 获取车辆可用性成功，找到 {len(vehicle_data)} 个可用车辆")
        
        return {
            "success": True,
            "vehicles": vehicle_data,
            "total_available": len(vehicle_data),
            "query_date": schedule_date.isoformat(),
            "shift_time": f"{shift_start} - {shift_end}",
            "task_type": task_type
        }
        
    except ValueError as e:
        logger.error(f"时间格式错误: {str(e)}")
        raise HTTPException(status_code=400, detail="时间格式错误，请使用 HH:MM 格式")
    except Exception as e:
        logger.error(f"获取车辆可用性失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取车辆可用性失败")