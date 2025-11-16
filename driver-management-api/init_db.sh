#!/bin/bash

# 创建数据库
echo "Creating database..."
mysql -u root -e "CREATE DATABASE IF NOT EXISTS driver_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 初始化管理员账户
echo "Initializing admin account..."
python -c "
import asyncio
import sys
sys.path.append('.')
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User

async def init_admin():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # 检查管理员是否已存在
        result = await session.execute(select(User).where(User.username == settings.ADMIN_USERNAME))
        admin_user = result.scalar_one_or_none()
        
        if not admin_user:
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                role='admin'
            )
            session.add(admin_user)
            await session.commit()
            print('Admin user created successfully!')
        else:
            print('Admin user already exists!')

if __name__ == '__main__':
    from sqlalchemy import select
    asyncio.run(init_admin())
"

echo "Database initialization completed!"