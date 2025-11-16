from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.api.v1 import api_router
from app.core.logging import setup_logging
from app.core.config import settings
from app.crud import get_user_by_username, update_user, create_user, create_operation_log
from app.core.security import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    setup_logging()
    # 重置管理员密码（如提供）
    if settings.DEFAULT_ADMIN_PASSWORD:
        async with AsyncSessionLocal() as session:
            admin = await get_user_by_username(session, settings.ADMIN_USERNAME)
            if admin:
                await update_user(session, admin.id, password_hash=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD))
                await create_operation_log(session, admin.id, 'password_reset', 'users', admin.id, None, None)
            else:
                await create_user(session, settings.ADMIN_USERNAME, settings.ADMIN_EMAIL, settings.DEFAULT_ADMIN_PASSWORD, 'admin')
    
    yield


app = FastAPI(
    title="司机管理系统API",
    description="基于FastAPI的司机管理后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# API路由
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "司机管理系统API服务运行正常", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={
        "code": 50000,
        "message": "服务器内部错误",
        "detail": str(exc)
    })