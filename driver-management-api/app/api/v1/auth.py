from datetime import datetime
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.core.security import create_access_token, verify_password, get_password_hash
from app.crud import create_operation_log
from app.models import User
from app.crud import (
    get_user_by_username, get_user_by_email, create_user, 
    get_user_by_id, get_users, update_user
)
from app.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """注册用户（管理员权限）"""
    # 检查用户名是否已存在
    user = await get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if user_in.email:
        user = await get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="邮箱已存在"
            )
    
    # 创建用户
    user = await create_user(
        db,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        role=user_in.role
    )
    
    return user


@router.post("/login")
async def login(
    form_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    username = form_data.get("username")
    password = form_data.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名和密码不能为空"
        )
    
    # 验证用户
    user = await get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    await create_operation_log(db, user.id, "login", "users", user.id)
    return {
        "token": access_token,
        "expires_in": 1800,
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户信息"""
    return current_user


@router.get("/", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取用户列表（管理员权限）"""
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取指定用户信息（管理员权限）"""
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """更新用户信息（管理员权限）"""
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    # 检查邮箱是否已存在
    if user_in.email:
        existing_user = await get_user_by_email(db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="邮箱已存在"
            )
    
    user = await update_user(db, user_id=user_id, **user_in.dict(exclude_unset=True))
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """删除用户（管理员权限）"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="不能删除自己的账户"
        )
    
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    await update_user(db, user_id=user_id, is_active=False)
    return {"message": "用户已禁用"}
@router.post("/change-password")
async def change_password(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    current = payload.get("current_password")
    new = payload.get("new_password")
    if not current or not new:
        raise HTTPException(status_code=400, detail="当前密码和新密码不能为空")
    if not verify_password(current, current_user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码不正确")
    current_user.password_hash = get_password_hash(new)
    await db.commit()
    await db.refresh(current_user)
    await create_operation_log(db, current_user.id, "password_change", "users", current_user.id)
    return {"message": "密码修改成功"}


@router.post("/reset-password")
async def reset_password(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    username = payload.get("username")
    new_password = payload.get("new_password")
    if not username or not new_password:
        raise HTTPException(status_code=400, detail="用户名和新密码不能为空")
    user = await get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.password_hash = get_password_hash(new_password)
    await db.commit()
    await db.refresh(user)
    await create_operation_log(db, current_user.id, "password_reset", "users", user.id)
    return {"message": "密码已重置"}