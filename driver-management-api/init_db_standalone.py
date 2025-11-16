#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
from app.core.config import settings
from app.core.security import get_password_hash
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="employee")
    is_active = Column(Boolean, default=True, index=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


async def init_database():
    """初始化数据库"""
    try:
        # 创建引擎
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        
        # 创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("数据库表创建成功")
        
        # 创建管理员账户
        async with engine.begin() as conn:
            # 检查管理员是否已存在
            result = await conn.execute(
                select(User).where(User.username == settings.ADMIN_USERNAME)
            )
            admin_user = result.scalar_one_or_none()
            
            if not admin_user:
                # 创建管理员
                admin_user = User(
                    username=settings.ADMIN_USERNAME,
                    email=settings.ADMIN_EMAIL,
                    password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                    role='admin'
                )
                conn.add(admin_user)
                await conn.commit()
                print('管理员账户创建成功!')
            else:
                print('管理员账户已存在!')
        
        await engine.dispose()
                
    except Exception as e:
        print(f"初始化失败: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(init_database())