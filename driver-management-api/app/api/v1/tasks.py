from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models import Task, TaskEvent, User
from app.crud import create_operation_log
from datetime import datetime

router = APIRouter()


@router.get("")
async def list_tasks(status: str | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    result = await db.execute(stmt.order_by(Task.created_at.desc()))
    return [t for t, in result.all()]


@router.get("/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.post("")
async def create_task(payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    task = Task(
        title=payload.get("title") or "未命名任务",
        description=payload.get("description") or None,
        assignee_id=payload.get("assignee_id") or None,
        due_date=(datetime.fromisoformat(payload["due_date"]) if payload.get("due_date") else None),
        priority=payload.get("priority") or "medium",
        status=payload.get("status") or "draft",
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    await create_operation_log(db, current_user.id, "task_create", "tasks", task.id, None, None)
    return task


@router.put("/{task_id}/assign")
async def assign_task(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    assignee_id = payload.get("assignee_id")
    if not assignee_id:
        raise HTTPException(status_code=400, detail="缺少 assignee_id")
    await db.execute(update(Task).where(Task.id == task_id).values(assignee_id=assignee_id, status="assigned"))
    event = TaskEvent(task_id=task_id, type="assign", content=f"assign to {assignee_id}", actor_id=current_user.id)
    db.add(event)
    await db.commit()
    await create_operation_log(db, current_user.id, "task_assign", "tasks", task_id, None, None)
    return {"message": "任务已分配"}


@router.post("/{task_id}/event")
async def add_task_event(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    evt_type = payload.get("type") or "note"
    content = payload.get("content") or None
    status = payload.get("status")
    event = TaskEvent(task_id=task_id, type=evt_type, content=content, actor_id=current_user.id)
    db.add(event)
    if status:
        await db.execute(update(Task).where(Task.id == task_id).values(status=status))
    await db.commit()
    if evt_type == "abnormal":
        await create_operation_log(db, current_user.id, "task_abnormal", "tasks", task_id, None, content)
    else:
        await create_operation_log(db, current_user.id, "task_event", "tasks", task_id, None, content)
    return {"message": "事件已记录"}