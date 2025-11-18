from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, update, delete
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User, Vehicle
from app.schemas import (
    VehicleCreate, VehicleUpdate, VehicleResponse,
    MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordResponse
)

router = APIRouter()


@router.get("/", response_model=List[VehicleResponse])
async def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, pattern="^(active|maintenance|retired)$"),
    vehicle_type: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取车辆列表"""
    logger.info(f"用户 {current_user.username} 请求车辆列表")
    stmt = select(Vehicle)
    conds = []
    if status:
        conds.append(Vehicle.status == status)
    if vehicle_type:
        conds.append(Vehicle.vehicle_type.ilike(f"%{vehicle_type}%"))
    if q:
        conds.append(or_(Vehicle.plate_number.ilike(f"%{q}%"), Vehicle.brand.ilike(f"%{q}%"), Vehicle.model.ilike(f"%{q}%")))
    if conds:
        stmt = stmt.where(and_(*conds))
    result = await db.execute(stmt.offset(skip).limit(limit).order_by(Vehicle.created_at.desc()))
    return [v for v, in result.all()]


@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建车辆"""
    logger.info(f"用户 {current_user.username} 尝试创建车辆")
    v = Vehicle(
        plate_number=vehicle.plate_number,
        vehicle_type=vehicle.vehicle_type,
        brand=vehicle.brand,
        model=vehicle.model,
        year=vehicle.year,
        color=vehicle.color,
        engine_number=vehicle.engine_number,
        vin_number=vehicle.vin_number,
        purchase_date=vehicle.purchase_date,
        registration_date=vehicle.registration_date,
        insurance_expiry=vehicle.insurance_expiry,
        annual_inspection_date=vehicle.annual_inspection_date,
        maintenance_due_date=vehicle.maintenance_due_date,
        mileage=vehicle.mileage,
        fuel_type=vehicle.fuel_type,
        fuel_consumption=vehicle.fuel_consumption,
        status=vehicle.status or "active",
        current_driver_id=vehicle.current_driver_id,
    )
    db.add(v)
    await db.commit()
    await db.refresh(v)
    return v


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取车辆详情"""
    logger.info(f"用户 {current_user.username} 请求车辆详情 ID: {vehicle_id}")
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    v = result.scalar_one_or_none()
    if not v:
        raise HTTPException(status_code=404, detail="车辆不存在")
    return v