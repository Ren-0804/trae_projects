from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.api.v1 import api_router
from app.core.logging import setup_logging
from app.core.config import settings
from app.crud import get_user_by_username, update_user, create_user, create_operation_log
from app.core.security import get_password_hash
from app.services.task_manager import task_manager
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Ensure region_type column exists
        try:
            result = await conn.execute(text("PRAGMA table_info(drivers)"))
            cols = [row[1] for row in result.fetchall()]
            if "region_type" not in cols:
                await conn.execute(text("ALTER TABLE drivers ADD COLUMN region_type VARCHAR(10) DEFAULT '国内'"))
        except Exception:
            pass
    
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
    
    # 启动后台任务管理器
    task_manager.start()
    
    yield
    
    # 应用关闭时停止后台任务
    task_manager.stop()


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

# 验证错误处理（记录统一JSON日志）
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 记录到操作日志
    try:
        async with AsyncSessionLocal() as session:
            await create_operation_log(session, 0, "validation_error", request.url.path, 0, None, str(exc))
    except Exception:
        pass

    # 汇总可读的错误消息
    errors = exc.errors()
    messages = []
    for e in errors:
        loc = ".".join(str(x) for x in e.get("loc", []))
        msg = e.get("msg", "验证错误")
        messages.append(f"{loc}: {msg}" if loc else msg)

    return JSONResponse(status_code=422, content={
        "code": 42200,
        "message": "; ".join(messages) if messages else "验证错误",
        "detail": errors,
    })