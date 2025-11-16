from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.models import User, Driver
from app.crud import (
    create_driver as crud_create_driver, get_drivers as crud_get_drivers, get_drivers_count, get_driver_by_id,
    update_driver as crud_update_driver, delete_driver as crud_delete_driver, get_driver_by_id_card, get_driver_by_license_number,
    create_driver_photo, get_driver_photos, delete_driver_photo
)
from app.schemas import DriverCreate, DriverUpdate, DriverResponse, DriverListResponse, DriverPhotoResponse
from app.core.config import settings
from app.utils.file import save_upload_file

router = APIRouter()


@router.get("/", response_model=DriverListResponse)
async def get_drivers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None),
    route: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取司机列表"""
    # 权限控制：普通员工只能查看自己的司机
    if current_user.role != "admin":
        user_id = current_user.id
    
    skip = (page - 1) * page_size
    
    drivers = await crud_get_drivers(
        db,
        user_id=user_id,
        keyword=keyword,
        route=route,
        status=status,
        skip=skip,
        limit=page_size
    )
    
    total = await get_drivers_count(
        db,
        user_id=user_id,
        keyword=keyword,
        route=route,
        status=status
    )
    
    return {
        "data": drivers,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取司机详情"""
    driver = await get_driver_by_id(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    # 权限控制：普通员工只能查看自己的司机
    if current_user.role != "admin" and driver.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return driver


@router.post("/", response_model=DriverResponse)
async def create_driver(
    driver_in: DriverCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建司机"""
    # 检查身份证号是否已存在
    existing_driver = await get_driver_by_id_card(db, id_card=driver_in.id_card)
    if existing_driver:
        raise HTTPException(status_code=400, detail="身份证号已存在")
    
    # 检查驾驶证号是否已存在
    existing_driver = await get_driver_by_license_number(db, license_number=driver_in.license_number)
    if existing_driver:
        raise HTTPException(status_code=400, detail="驾驶证号已存在")
    
    # 创建司机
    driver_data = driver_in.dict()
    driver_data['user_id'] = current_user.id
    driver = await crud_create_driver(db, **driver_data)
    
    return driver


@router.put("/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: int,
    driver_in: DriverUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新司机信息"""
    driver = await get_driver_by_id(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    # 权限控制：普通员工只能更新自己的司机
    if current_user.role != "admin" and driver.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 检查身份证号是否已存在（如果更新的话）
    if driver_in.id_card and driver_in.id_card != driver.id_card:
        existing_driver = await get_driver_by_id_card(db, id_card=driver_in.id_card)
        if existing_driver:
            raise HTTPException(status_code=400, detail="身份证号已存在")
    
    # 检查驾驶证号是否已存在（如果更新的话）
    if driver_in.license_number and driver_in.license_number != driver.license_number:
        existing_driver = await get_driver_by_license_number(db, license_number=driver_in.license_number)
        if existing_driver:
            raise HTTPException(status_code=400, detail="驾驶证号已存在")
    
    # 更新司机
    driver = await crud_update_driver(
        db,
        driver_id=driver_id,
        **driver_in.dict(exclude_unset=True)
    )
    
    return driver


@router.delete("/{driver_id}")
async def delete_driver(
    driver_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除司机"""
    driver = await get_driver_by_id(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    # 权限控制：普通员工只能删除自己的司机
    if current_user.role != "admin" and driver.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    success = await crud_delete_driver(db, driver_id=driver_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除失败")
    
    return {"message": "司机已删除"}


@router.post("/{driver_id}/photos", response_model=DriverPhotoResponse)
async def upload_driver_photo(
    driver_id: int,
    photo_type: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """上传司机照片"""
    driver = await get_driver_by_id(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    # 权限控制：普通员工只能上传自己的司机照片
    if current_user.role != "admin" and driver.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 验证照片类型
    valid_types = ["id_card_front", "id_card_back", "license", "vehicle"]
    if photo_type not in valid_types:
        raise HTTPException(status_code=400, detail="无效的照片类型")
    
    # 保存文件
    file_path = await save_upload_file(file, settings.UPLOAD_DIR)
    
    # 创建照片记录
    photo = await create_driver_photo(
        db,
        driver_id=driver_id,
        photo_type=photo_type,
        file_path=file_path,
        file_name=file.filename,
        file_size=file.size,
        mime_type=file.content_type
    )
    
    return photo


@router.get("/{driver_id}/photos", response_model=List[DriverPhotoResponse])
async def get_driver_photos(
    driver_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取司机照片列表"""
    driver = await get_driver_by_id(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    # 权限控制：普通员工只能查看自己的司机照片
    if current_user.role != "admin" and driver.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    photos = await get_driver_photos(db, driver_id=driver_id)
    return photos


@router.get("/photos/{photo_id}")
async def serve_driver_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取司机照片文件"""
    from app.models import DriverPhoto
    from fastapi.responses import FileResponse
    
    photo = await db.get(DriverPhoto, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在")
    
    # 权限控制：普通员工只能查看自己的司机照片
    driver = await get_driver_by_id(db, driver_id=photo.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    if current_user.role != "admin" and driver.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return FileResponse(photo.file_path)