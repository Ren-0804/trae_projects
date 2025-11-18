from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from io import StringIO
from app.core.database import get_db
from app.core.deps import get_current_admin_user
from app.models import OperationLog, User
from app.crud import create_operation_log
import json

router = APIRouter()


@router.get("/logs")
async def get_logs(user_id: int | None = None, operation_type: str | None = None, start: str | None = None, end: str | None = None, format: str | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    from sqlalchemy import and_
    stmt = select(OperationLog)
    conds = []
    if user_id:
        conds.append(OperationLog.user_id == user_id)
    if operation_type:
        conds.append(OperationLog.operation_type == operation_type)
    if start:
        from datetime import datetime
        conds.append(OperationLog.created_at >= datetime.fromisoformat(start))
    if end:
        from datetime import datetime
        conds.append(OperationLog.created_at <= datetime.fromisoformat(end))
    if conds:
        stmt = stmt.where(and_(*conds))
    result = await db.execute(stmt.order_by(OperationLog.created_at.desc()))
    rows = [r for r, in result.all()]
    if format == "csv":
        out = StringIO()
        out.write("id,operation_type,user_id,table_name,record_id,created_at,hash,prev_hash\n")
        for r in rows:
            out.write(f"{r.id},{r.operation_type},{r.user_id},{r.table_name},{r.record_id},{r.created_at},{r.hash or ''},{r.prev_hash or ''}\n")
        return Response(content=out.getvalue(), media_type="text/csv")
    return rows


@router.get("/logs/{log_id}")
async def get_log(log_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    result = await db.execute(select(OperationLog).where(OperationLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    return log


@router.post("/logs")
async def create_log(payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    actor_id = int(payload.get("actor_id") or current_user.id)
    action = str(payload.get("action") or "custom")
    resource = str(payload.get("resource") or "unknown")
    resource_id = payload.get("resource_id")
    try:
        record_id = int(resource_id) if resource_id is not None else 0
    except Exception:
        record_id = 0
    content = payload.get("content")
    new_data = json.dumps(content) if content is not None else None
    log = await create_operation_log(db, actor_id, action, resource, record_id, None, new_data)
    return {"id": log.id}


@router.post("/alerts")
async def create_alert(payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    actor_id = int(payload.get("actor_id") or current_user.id)
    action = str(payload.get("action") or "alert")
    resource = str(payload.get("resource") or "unknown")
    resource_id = payload.get("resource_id")
    try:
        record_id = int(resource_id) if resource_id is not None else 0
    except Exception:
        record_id = 0
    description = payload.get("description")
    severity = payload.get("severity")
    data = {"description": description, "severity": severity}
    log = await create_operation_log(db, actor_id, action, resource, record_id, None, json.dumps(data))
    return {"id": log.id}


@router.get("/stats")
async def audit_stats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    from sqlalchemy import func
    ops = (await db.execute(select(OperationLog.operation_type, func.count(OperationLog.id)).group_by(OperationLog.operation_type))).all()
    tables = (await db.execute(select(OperationLog.table_name, func.count(OperationLog.id)).group_by(OperationLog.table_name))).all()
    users = (await db.execute(select(OperationLog.user_id, func.count(OperationLog.id)).group_by(OperationLog.user_id))).all()
    return {"by_operation": ops, "by_table": tables, "by_user": users}