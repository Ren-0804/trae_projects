from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta, date

from app.models import User, Driver, DriverPhoto, OperationLog, Schedule, Vehicle, DriverCertificate
from app.core.security import get_password_hash, verify_password


# User CRUD operations
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, email: Optional[str], password: str, role: str = "employee") -> User:
    user = User(
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        role=role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, **kwargs) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    
    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def get_users_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(User.id)))
    return result.scalar()


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """真正删除用户"""
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    
    await db.delete(user)
    await db.commit()
    return True


# Driver CRUD operations
async def get_driver_by_id(db: AsyncSession, driver_id: int) -> Optional[Driver]:
    result = await db.execute(select(Driver).where(Driver.id == driver_id))
    return result.scalar_one_or_none()


async def get_driver_by_id_card(db: AsyncSession, id_card: str) -> Optional[Driver]:
    result = await db.execute(select(Driver).where(Driver.id_card == id_card))
    return result.scalar_one_or_none()


async def get_driver_by_license_number(db: AsyncSession, license_number: str) -> Optional[Driver]:
    result = await db.execute(select(Driver).where(Driver.license_number == license_number))
    return result.scalar_one_or_none()


async def create_driver(db: AsyncSession, **kwargs) -> Driver:
    driver = Driver(**kwargs)
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


async def update_driver(db: AsyncSession, driver_id: int, **kwargs) -> Optional[Driver]:
    driver = await get_driver_by_id(db, driver_id)
    if not driver:
        return None
    
    for key, value in kwargs.items():
        if hasattr(driver, key) and value is not None:
            setattr(driver, key, value)
    
    driver.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(driver)
    return driver


async def delete_driver(db: AsyncSession, driver_id: int) -> bool:
    driver = await get_driver_by_id(db, driver_id)
    if not driver:
        return False
    
    await db.delete(driver)
    await db.commit()
    return True


async def get_drivers(
    db: AsyncSession, 
    user_id: Optional[int] = None,
    keyword: Optional[str] = None,
    route: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0, 
    limit: int = 20
) -> List[Driver]:
    query = select(Driver)
    
    # 权限过滤
    if user_id:
        query = query.where(Driver.user_id == user_id)
    
    # 搜索过滤
    if keyword:
        query = query.where(
            or_(
                Driver.name.contains(keyword),
                Driver.phone.contains(keyword),
                Driver.main_route.contains(keyword)
            )
        )
    
    # 线路过滤
    if route:
        query = query.where(Driver.main_route.contains(route))
    
    # 状态过滤
    if status:
        query = query.where(Driver.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Driver.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Schedule CRUD operations
async def get_schedules(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    driver_id: Optional[int] = None,
    vehicle_id: Optional[int] = None,
    schedule_date: Optional[date] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    task_type: Optional[str] = None
) -> List[Schedule]:
    query = select(Schedule)
    
    if driver_id:
        query = query.where(Schedule.driver_id == driver_id)
    if vehicle_id:
        query = query.where(Schedule.vehicle_id == vehicle_id)
    if schedule_date:
        query = query.where(
            Schedule.schedule_date >= datetime.combine(schedule_date, datetime.min.time()),
            Schedule.schedule_date < datetime.combine(schedule_date + timedelta(days=1), datetime.min.time())
        )
    if start_date:
        query = query.where(Schedule.schedule_date >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(Schedule.schedule_date < datetime.combine(end_date + timedelta(days=1), datetime.min.time()))
    if status:
        query = query.where(Schedule.status == status)
    if task_type:
        query = query.where(Schedule.task_type == task_type)
    
    query = query.order_by(Schedule.schedule_date.desc(), Schedule.start_time.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_schedule_by_id(db: AsyncSession, schedule_id: int) -> Optional[Schedule]:
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    return result.scalar_one_or_none()


async def create_schedule(db: AsyncSession, **kwargs) -> Schedule:
    schedule = Schedule(**kwargs)
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


async def update_schedule(db: AsyncSession, schedule_id: int, **kwargs) -> Optional[Schedule]:
    schedule = await get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None
    
    for key, value in kwargs.items():
        if hasattr(schedule, key) and value is not None:
            setattr(schedule, key, value)
    
    schedule.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(schedule)
    return schedule


async def delete_schedule(db: AsyncSession, schedule_id: int) -> bool:
    schedule = await get_schedule_by_id(db, schedule_id)
    if not schedule:
        return False
    
    await db.delete(schedule)
    await db.commit()
    return True


# Vehicle CRUD operations
async def get_vehicles(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    vehicle_type: Optional[str] = None
) -> List[Vehicle]:
    query = select(Vehicle)
    
    if status:
        query = query.where(Vehicle.status == status)
    if vehicle_type:
        query = query.where(Vehicle.vehicle_type == vehicle_type)
    
    query = query.offset(skip).limit(limit).order_by(Vehicle.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


async def get_vehicle_by_id(db: AsyncSession, vehicle_id: int) -> Optional[Vehicle]:
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    return result.scalar_one_or_none()


async def create_vehicle(db: AsyncSession, **kwargs) -> Vehicle:
    vehicle = Vehicle(**kwargs)
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def update_vehicle(db: AsyncSession, vehicle_id: int, **kwargs) -> Optional[Vehicle]:
    vehicle = await get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        return None
    
    for key, value in kwargs.items():
        if hasattr(vehicle, key) and value is not None:
            setattr(vehicle, key, value)
    
    vehicle.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def delete_vehicle(db: AsyncSession, vehicle_id: int) -> bool:
    vehicle = await get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        return False
    
    await db.delete(vehicle)
    await db.commit()
    return True


# DriverCertificate CRUD operations
async def get_certificates(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    driver_id: Optional[int] = None,
    certificate_type: Optional[str] = None,
    status: Optional[str] = None,
    expiring_soon: bool = False,
    days_ahead: int = 30
) -> List[DriverCertificate]:
    query = select(DriverCertificate)
    
    if driver_id:
        query = query.where(DriverCertificate.driver_id == driver_id)
    if certificate_type:
        query = query.where(DriverCertificate.certificate_type == certificate_type)
    if status:
        query = query.where(DriverCertificate.status == status)
    
    if expiring_soon:
        expiry_date = datetime.utcnow() + timedelta(days=days_ahead)
        query = query.where(DriverCertificate.expiry_date <= expiry_date)
    
    query = query.offset(skip).limit(limit).order_by(DriverCertificate.expiry_date.asc())
    result = await db.execute(query)
    return result.scalars().all()


async def get_certificate_by_id(db: AsyncSession, certificate_id: int) -> Optional[DriverCertificate]:
    result = await db.execute(select(DriverCertificate).where(DriverCertificate.id == certificate_id))
    return result.scalar_one_or_none()


async def create_certificate(db: AsyncSession, **kwargs) -> DriverCertificate:
    certificate = DriverCertificate(**kwargs)
    db.add(certificate)
    await db.commit()
    await db.refresh(certificate)
    return certificate


async def update_certificate(db: AsyncSession, certificate_id: int, **kwargs) -> Optional[DriverCertificate]:
    certificate = await get_certificate_by_id(db, certificate_id)
    if not certificate:
        return None
    
    for key, value in kwargs.items():
        if hasattr(certificate, key) and value is not None:
            setattr(certificate, key, value)
    
    certificate.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(certificate)
    return certificate


async def delete_certificate(db: AsyncSession, certificate_id: int) -> bool:
    certificate = await get_certificate_by_id(db, certificate_id)
    if not certificate:
        return False
    
    await db.delete(certificate)
    await db.commit()
    return certificate


async def get_drivers_count(
    db: AsyncSession,
    user_id: Optional[int] = None,
    keyword: Optional[str] = None,
    route: Optional[str] = None,
    status: Optional[str] = None
) -> int:
    query = select(func.count(Driver.id))
    
    if user_id:
        query = query.where(Driver.user_id == user_id)
    
    if keyword:
        query = query.where(
            or_(
                Driver.name.contains(keyword),
                Driver.phone.contains(keyword),
                Driver.main_route.contains(keyword)
            )
        )
    
    if route:
        query = query.where(Driver.main_route.contains(route))
    
    if status:
        query = query.where(Driver.status == status)
    
    result = await db.execute(query)
    return result.scalar()


# Driver Photo CRUD operations
async def create_driver_photo(db: AsyncSession, driver_id: int, **kwargs) -> DriverPhoto:
    photo = DriverPhoto(driver_id=driver_id, **kwargs)
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


async def get_driver_photos(db: AsyncSession, driver_id: int) -> List[DriverPhoto]:
    result = await db.execute(select(DriverPhoto).where(DriverPhoto.driver_id == driver_id))
    return result.scalars().all()


async def delete_driver_photo(db: AsyncSession, photo_id: int) -> bool:
    result = await db.execute(select(DriverPhoto).where(DriverPhoto.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        return False
    
    await db.delete(photo)
    await db.commit()
    return True


# Operation Log CRUD operations
async def create_operation_log(db: AsyncSession, user_id: int, operation_type: str, 
                             table_name: str, record_id: int, old_data: Optional[str] = None,
                             new_data: Optional[str] = None, ip_address: Optional[str] = None,
                             user_agent: Optional[str] = None) -> OperationLog:
    log = OperationLog(
        user_id=user_id,
        operation_type=operation_type,
        table_name=table_name,
        record_id=record_id,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def get_operation_logs(db: AsyncSession, user_id: Optional[int] = None,
                           table_name: Optional[str] = None, skip: int = 0, 
                           limit: int = 50) -> List[OperationLog]:
    query = select(OperationLog)
    
    if user_id:
        query = query.where(OperationLog.user_id == user_id)
    
    if table_name:
        query = query.where(OperationLog.table_name == table_name)
    
    query = query.offset(skip).limit(limit).order_by(OperationLog.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()