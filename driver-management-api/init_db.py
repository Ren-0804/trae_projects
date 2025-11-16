#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User


async def init_database():
    """初始化数据库"""
    try:
        # 创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("数据库表创建成功")
        
        # 创建管理员账户
        async with AsyncSessionLocal() as session:
            # 检查管理员是否已存在
            result = await session.execute(
                select(User).where(User.username == settings.ADMIN_USERNAME)
            )
            admin_user = result.scalar_one_or_none()
            
            if not admin_user:
                # 创建管理员
                admin_user = User(
                    username=settings.ADMIN_USERNAME,
                    email=settings.ADMIN_EMAIL,
                    password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                    role='admin',
                    is_active=True
                )
                session.add(admin_user)
                await session.commit()
                print('管理员账户创建成功!')
            else:
                print('管理员账户已存在!')
                
    except Exception as e:
        print(f"初始化失败: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == '__main__':
    asyncio.run(init_database())