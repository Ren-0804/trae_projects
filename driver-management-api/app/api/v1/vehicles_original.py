from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User, Vehicle, VehicleAssignment, Driver, MaintenanceRecord
from app.schemas import (
    VehicleCreate, VehicleUpdate, VehicleResponse,
    MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordResponse
)
from app.crud import (
    get_vehicles as crud_get_vehicles, get_vehicle_by_id as crud_get_vehicle_by_id,
    create_vehicle as crud_create_vehicle, update_vehicle as crud_update_vehicle,
    delete_vehicle as crud_delete_vehicle,
    create_operation_log
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=List[VehicleResponse])
async def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, pattern="^(active|maintenance|retired)$"),
    vehicle_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取车辆列表"""
    try:
        vehicles = await crud_get_vehicles(
            db=db,
            skip=skip,
            limit=limit,
            status=status,
            vehicle_type=vehicle_type
        )
        
        logger.info(f"用户 {current_user.username} 获取了 {len(vehicles)} 条车辆记录")
        return vehicles
        
    except Exception as e:
        logger.error(f"获取车辆列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取车辆列表失败")


@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建车辆"""
    try:
        # 检查车牌号是否已存在
        existing = db.query(Vehicle).filter(Vehicle.plate_number == vehicle.plate_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="车牌号已存在")
            
        # 检查VIN号是否已存在
        if vehicle.vin_number:
            existing_vin = db.query(Vehicle).filter(Vehicle.vin_number == vehicle.vin_number).first()
            if existing_vin:
                raise HTTPException(status_code=400, detail="VIN号已存在")
        
        db_vehicle = Vehicle(**vehicle.dict())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="create",
            table_name="vehicles",
            record_id=db_vehicle.id,
            old_data=None,
            new_data=vehicle.json()
        )
        
        logger.info(f"用户 {current_user.username} 创建了车辆 {vehicle.plate_number}")
        return db_vehicle
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建车辆失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建车辆失败")


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取车辆详情"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
        
        # 获取司机分配记录
        assignments = db.query(VehicleAssignment).filter(
            VehicleAssignment.vehicle_id == vehicle_id
        ).order_by(VehicleAssignment.start_date.desc()).all()
        
        # 构建响应数据
        vehicle_data = {
            **vehicle.__dict__,
            'assignments': []
        }
        
        # 添加分配记录
        for assignment in assignments:
            assignment_data = {
                'id': assignment.id,
                'driver_id': assignment.driver_id,
                'assignment_type': assignment.assignment_type,
                'start_date': assignment.start_date,
                'end_date': assignment.end_date,
                'status': assignment.status,
                'driver': {
                    'id': assignment.driver.id,
                    'name': assignment.driver.name,
                    'phone': assignment.driver.phone,
                    'license_number': assignment.driver.license_number
                } if assignment.driver else None
            }
            vehicle_data['assignments'].append(assignment_data)
        
        logger.info(f"用户 {current_user.username} 查看了车辆 {vehicle.plate_number}")
        return vehicle_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取车辆详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取车辆详情失败")


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新车辆信息"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        # 检查车牌号是否已存在（如果更新车牌号）
        if vehicle_update.plate_number and vehicle_update.plate_number != vehicle.plate_number:
            existing = db.query(Vehicle).filter(
                Vehicle.plate_number == vehicle_update.plate_number,
                Vehicle.id != vehicle_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="车牌号已存在")
                
        # 检查VIN号是否已存在（如果更新VIN号）
        if vehicle_update.vin_number and vehicle_update.vin_number != vehicle.vin_number:
            existing_vin = db.query(Vehicle).filter(
                Vehicle.vin_number == vehicle_update.vin_number,
                Vehicle.id != vehicle_id
            ).first()
            if existing_vin:
                raise HTTPException(status_code=400, detail="VIN号已存在")
        
        # 记录旧数据
        old_data = vehicle.json()
        
        # 更新字段
        update_data = vehicle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vehicle, field, value)
            
        vehicle.updated_at = datetime.now()
        db.commit()
        db.refresh(vehicle)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="update",
            table_name="vehicles",
            record_id=vehicle_id,
            old_data=old_data,
            new_data=vehicle.json()
        )
        
        logger.info(f"用户 {current_user.username} 更新了车辆 {vehicle.plate_number}")
        return vehicle
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新车辆失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新车辆失败")


@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除车辆"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        # 记录车辆信息用于日志
        vehicle_data = vehicle.json()
        plate_number = vehicle.plate_number
        
        db.delete(vehicle)
        db.commit()
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="delete",
            table_name="vehicles",
            record_id=vehicle_id,
            old_data=vehicle_data,
            new_data=None
        )
        
        logger.info(f"用户 {current_user.username} 删除了车辆 {plate_number}")
        return {"message": "车辆删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除车辆失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除车辆失败")


@router.post("/{vehicle_id}/assign-driver")
async def assign_driver_to_vehicle(
    vehicle_id: int,
    driver_id: int,
    assignment_type: str = Query("primary", pattern="^(primary|temporary)$"),
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """分配司机到车辆"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        # 检查是否已有活跃分配
        existing_assignment = db.query(VehicleAssignment).filter(
            VehicleAssignment.vehicle_id == vehicle_id,
            VehicleAssignment.driver_id == driver_id,
            VehicleAssignment.status == "active"
        ).first()
        
        if existing_assignment:
            raise HTTPException(status_code=400, detail="该司机已分配到此车辆")
            
        # 创建新的分配记录
        assignment = VehicleAssignment(
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            assignment_type=assignment_type,
            start_date=datetime.now(),
            end_date=end_date,
            status="active"
        )
        
        # 如果是主要分配，更新车辆的当前司机
        if assignment_type == "primary":
            vehicle.current_driver_id = driver_id
            
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        
        logger.info(f"用户 {current_user.username} 将司机 {driver.name} 分配到车辆 {vehicle.plate_number}")
        return assignment
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"分配司机失败: {str(e)}")
        raise HTTPException(status_code=500, detail="分配司机失败")


@router.put("/{vehicle_id}/assignments/{assignment_id}/end")
async def end_driver_assignment(
    vehicle_id: int,
    assignment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """结束司机分配"""
    try:
        assignment = db.query(VehicleAssignment).filter(
            VehicleAssignment.id == assignment_id,
            VehicleAssignment.vehicle_id == vehicle_id
        ).first()
        
        if not assignment:
            raise HTTPException(status_code=404, detail="分配记录不存在")
            
        if assignment.status != "active":
            raise HTTPException(status_code=400, detail="该分配已结束")
            
        # 结束分配
        assignment.status = "ended"
        assignment.end_date = datetime.now()
        
        # 如果是主要分配，清除车辆的当前司机
        if assignment.assignment_type == "primary":
            vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
            if vehicle and vehicle.current_driver_id == assignment.driver_id:
                vehicle.current_driver_id = None
        
        db.commit()
        db.refresh(assignment)
        
        logger.info(f"用户 {current_user.username} 结束了司机分配 {assignment_id}")
        return assignment
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"结束司机分配失败: {str(e)}")
        raise HTTPException(status_code=500, detail="结束司机分配失败")


@router.get("/{vehicle_id}/maintenance-records", response_model=List[MaintenanceRecordResponse])
async def get_vehicle_maintenance_records(
    vehicle_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取车辆维护记录"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        records = db.query(MaintenanceRecord).filter(
            MaintenanceRecord.vehicle_id == vehicle_id
        ).order_by(MaintenanceRecord.service_date.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"用户 {current_user.username} 获取了车辆 {vehicle.plate_number} 的 {len(records)} 条维护记录")
        return records
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取维护记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取维护记录失败")


@router.post("/{vehicle_id}/maintenance-records", response_model=MaintenanceRecordResponse)
async def create_maintenance_record(
    vehicle_id: int,
    record: MaintenanceRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建维护记录"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        db_record = MaintenanceRecord(**record.dict())
        db.add(db_record)
        
        # 更新车辆的下次维护日期
        if record.next_service_date:
            vehicle.maintenance_due_date = record.next_service_date
            
        db.commit()
        db.refresh(db_record)
        
        logger.info(f"用户 {current_user.username} 为车辆 {vehicle.plate_number} 创建了维护记录")
        return db_record
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建维护记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建维护记录失败")


@router.get("/maintenance/upcoming")
async def get_upcoming_maintenance(
    days_ahead: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取即将到期的维护提醒"""
    try:
        today = datetime.now().date()
        future_date = today + timedelta(days=days_ahead)
        
        vehicles = db.query(Vehicle).filter(
            Vehicle.maintenance_due_date >= today,
            Vehicle.maintenance_due_date <= future_date,
            Vehicle.status == "active"
        ).all()
        
        result = []
        for vehicle in vehicles:
            days_until = (vehicle.maintenance_due_date.date() - today).days
            result.append({
                "vehicle_id": vehicle.id,
                "plate_number": vehicle.plate_number,
                "maintenance_due_date": vehicle.maintenance_due_date,
                "days_until_maintenance": days_until,
                "urgency": "high" if days_until <= 7 else "medium" if days_until <= 14 else "low"
            })
        
        logger.info(f"用户 {current_user.username} 获取了 {len(result)} 条即将到期的维护提醒")
        return result
        
    except Exception as e:
        logger.error(f"获取维护提醒失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取维护提醒失败")


@router.get("/insurance/expiring")
async def get_expiring_insurance(
    days_ahead: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取即将到期的保险提醒"""
    try:
        today = datetime.now().date()
        future_date = today + timedelta(days=days_ahead)
        
        vehicles = db.query(Vehicle).filter(
            Vehicle.insurance_expiry >= today,
            Vehicle.insurance_expiry <= future_date,
            Vehicle.status == "active"
        ).all()
        
        result = []
        for vehicle in vehicles:
            days_until = (vehicle.insurance_expiry.date() - today).days
            result.append({
                "vehicle_id": vehicle.id,
                "plate_number": vehicle.plate_number,
                "insurance_expiry": vehicle.insurance_expiry,
                "days_until_expiry": days_until,
                "urgency": "high" if days_until <= 7 else "medium" if days_until <= 14 else "low"
            })
        
        logger.info(f"用户 {current_user.username} 获取了 {len(result)} 条即将到期的保险提醒")
        return result
        
    except Exception as e:
        logger.error(f"获取保险提醒失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取保险提醒失败")


@router.get("/assignments")
async def get_vehicle_assignments(
    vehicle_id: int = Query(..., description="车辆ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
    status: Optional[str] = Query(None, description="状态筛选"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取车辆司机分配记录"""
    try:
        # 验证车辆存在
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
        
        # 构建查询
        query = db.query(VehicleAssignment).filter(
            VehicleAssignment.vehicle_id == vehicle_id
        )
        
        # 应用筛选条件
        if status:
            query = query.filter(VehicleAssignment.status == status)
        if start_date:
            query = query.filter(VehicleAssignment.start_date >= start_date)
        if end_date:
            query = query.filter(VehicleAssignment.start_date <= end_date)
        
        # 计算总数
        total = query.count()
        
        # 分页查询
        assignments = query.order_by(
            VehicleAssignment.start_date.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()
        
        # 构建响应数据
        assignment_data = []
        for assignment in assignments:
            # 获取司机信息
            driver = db.query(Driver).filter(Driver.id == assignment.driver_id).first()
            
            # 计算使用统计
            start_date_obj = assignment.start_date
            end_date_obj = assignment.end_date or datetime.now()
            total_days = (end_date_obj.date() - start_date_obj.date()).days + 1
            
            assignment_info = {
                'id': assignment.id,
                'driver_id': assignment.driver_id,
                'assignment_type': assignment.assignment_type,
                'start_date': assignment.start_date.isoformat(),
                'end_date': assignment.end_date.isoformat() if assignment.end_date else None,
                'status': assignment.status,
                'created_at': assignment.created_at.isoformat(),
                'total_days': total_days,
                'is_active': assignment.status == 'active',
                'driver': {
                    'id': driver.id,
                    'name': driver.name,
                    'phone': driver.phone,
                    'license_number': driver.license_number,
                    'experience_years': driver.experience_years
                } if driver else None
            }
            assignment_data.append(assignment_info)
        
        logger.info(f"用户 {current_user.username} 获取了车辆 {vehicle.plate_number} 的 {len(assignment_data)} 条分配记录")
        
        return {
            "success": True,
            "data": assignment_data,
            "total": total,
            "page": page,
            "page_size": page_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取车辆分配记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取车辆分配记录失败")