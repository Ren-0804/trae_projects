from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models import Task, TaskEvent, TaskComment, TaskDependency, FileAsset, User
from app.crud import create_operation_log
from datetime import datetime
import json
from fastapi.responses import StreamingResponse, Response

router = APIRouter()


@router.get("")
async def list_tasks(status: str | None = None, q: str | None = None, assignee_id: int | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    stmt = select(Task)
    conds = []
    if status:
        conds.append(Task.status == status)
    if assignee_id:
        conds.append(Task.assignee_id == assignee_id)
    if q:
        conds.append(or_(Task.title.ilike(f"%{q}%"), Task.description.ilike(f"%{q}%")))
    if conds:
        stmt = stmt.where(and_(*conds))
    result = await db.execute(stmt.order_by(Task.sort_index.asc(), Task.created_at.desc()))
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
    # 生成任务编号
    now = datetime.utcnow()
    date_prefix = now.strftime("%Y%m%d")
    seq = (await db.execute(select(func.count(Task.id)).where(func.date(Task.created_at) == func.date(now)))).scalar() or 0
    task_no = f"T-{date_prefix}-{seq+1:04d}"
    task = Task(
        title=payload.get("title") or "未命名任务",
        description=payload.get("description") or None,
        assignee_id=payload.get("assignee_id") or None,
        due_date=(datetime.fromisoformat(payload["due_date"]) if payload.get("due_date") else None),
        priority=payload.get("priority") or "medium",
        status=payload.get("status") or "todo",
        sort_index=int(payload.get("sort_index") or 0),
        labels=(",".join(payload.get("labels") or []) or None),
        custom_fields=(json.dumps(payload.get("custom_fields")) if payload.get("custom_fields") else None),
        task_no=task_no,
        origin_address=payload.get("origin_address"),
        origin_lat=payload.get("origin_lat"),
        origin_lng=payload.get("origin_lng"),
        destination_address=payload.get("destination_address"),
        destination_lat=payload.get("destination_lat"),
        destination_lng=payload.get("destination_lng"),
        estimated_distance_km=payload.get("estimated_distance_km"),
        estimated_duration_min=payload.get("estimated_duration_min"),
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


@router.post("/{task_id}/status")
async def update_status(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    status = str(payload.get("status") or "")
    remark = payload.get("remark")
    timestamp = datetime.utcnow().isoformat()
    await db.execute(update(Task).where(Task.id == task_id).values(status=status))
    e = TaskEvent(task_id=task_id, type="update_status", content=json.dumps({"status": status, "remark": remark, "ts": timestamp}), actor_id=current_user.id)
    db.add(e)
    await db.commit()
    await create_operation_log(db, current_user.id, "task_status", "tasks", task_id, None, json.dumps({"status": status}))
    return {"message": "status updated", "ts": timestamp}


@router.get("/{task_id}/report")
async def task_report(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    t = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")
    events = (await db.execute(select(TaskEvent).where(TaskEvent.task_id == task_id).order_by(TaskEvent.created_at.asc()))).all()
    timeline = [json.loads(e.content or "{}") for e, in events if e.type in ("update_status","assign","move","comment")]
    return {
        "task": t,
        "timeline": timeline,
    }


@router.get("/{task_id}/report", response_model=None)
async def task_report_export(task_id: int, format: str | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    t = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")
    events = (await db.execute(select(TaskEvent).where(TaskEvent.task_id == task_id).order_by(TaskEvent.created_at.asc()))).all()
    if format == 'csv':
        rows = ["time,type,content"]
        for e, in events:
            rows.append(f"{e.created_at},{e.type},\"{(e.content or '').replace('"','') }\"")
        return Response(content="\n".join(rows), media_type="text/csv")
    timeline = [json.loads(e.content or "{}") for e, in events]
    return {"task": t, "timeline": timeline}


@router.post("/{task_id}/location")
async def update_location(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    lat = payload.get("lat")
    lng = payload.get("lng")
    if lat is None or lng is None:
        raise HTTPException(status_code=400, detail="缺少坐标")
    data = {"lat": lat, "lng": lng, "ts": datetime.utcnow().isoformat()}
    e = TaskEvent(task_id=task_id, type="location", content=json.dumps(data), actor_id=current_user.id)
    db.add(e)
    await db.commit()
    await create_operation_log(db, current_user.id, "task_location", "tasks", task_id, None, json.dumps(data))
    return {"message": "ok", "data": data}


@router.get("/{task_id}/sse")
async def task_sse(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    async def event_gen():
        import asyncio
        for _ in range(10):
            t = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
            loc = (await db.execute(select(TaskEvent).where(TaskEvent.task_id == task_id).where(TaskEvent.type == 'location').order_by(TaskEvent.created_at.desc()).limit(1))).first()
            payload = {"status": t.status if t else None, "location": json.loads(loc[0].content) if loc else None}
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(2)
    return StreamingResponse(event_gen(), media_type="text/event-stream")


@router.post("/{task_id}/comments")
async def add_comment(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    content = str(payload.get("content") or "")
    mentions = ",".join(payload.get("mentions") or []) or None
    if not content:
        raise HTTPException(status_code=400, detail="内容不能为空")
    c = TaskComment(task_id=task_id, content=content, mentions=mentions, creator_id=current_user.id)
    db.add(c)
    e = TaskEvent(task_id=task_id, type="comment", content=content, actor_id=current_user.id)
    db.add(e)
    await db.commit()
    await create_operation_log(db, current_user.id, "task_comment", "tasks", task_id, None, content)
    return {"id": c.id}


@router.get("/{task_id}/comments")
async def list_comments(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(TaskComment).where(TaskComment.task_id == task_id).order_by(TaskComment.created_at.asc()))
    return [c for c, in result.all()]


@router.post("/{task_id}/move")
async def move_task(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    status = payload.get("status")
    sort_index = int(payload.get("sort_index") or 0)
    await db.execute(update(Task).where(Task.id == task_id).values(status=status, sort_index=sort_index))
    e = TaskEvent(task_id=task_id, type="move", content=json.dumps({"status": status, "sort_index": sort_index}), actor_id=current_user.id)
    db.add(e)
    await db.commit()
    await create_operation_log(db, current_user.id, "task_move", "tasks", task_id, None, json.dumps({"status": status}))
    return {"message": "moved"}


@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    total = (await db.execute(select(func.count(Task.id)))).scalar()
    by_status = (await db.execute(select(Task.status, func.count(Task.id)).group_by(Task.status))).all()
    by_priority = (await db.execute(select(Task.priority, func.count(Task.id)).group_by(Task.priority))).all()
    return {"total": total, "by_status": by_status, "by_priority": by_priority}
@router.put("/{task_id}")
async def update_task(task_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updates = {}
    for k in ["title","description","assignee_id","priority","status","sort_index"]:
        if k in payload:
            updates[k] = payload[k]
    if "due_date" in payload:
        updates["due_date"] = datetime.fromisoformat(payload["due_date"]) if payload["due_date"] else None
    if "labels" in payload:
        updates["labels"] = ",".join(payload.get("labels") or []) or None
    if "custom_fields" in payload:
        updates["custom_fields"] = json.dumps(payload.get("custom_fields")) if payload.get("custom_fields") else None
    await db.execute(update(Task).where(Task.id == task_id).values(**updates))
    event = TaskEvent(task_id=task_id, type="update", content=json.dumps(updates), actor_id=current_user.id)
    db.add(event)
    await db.commit()
    await create_operation_log(db, current_user.id, "task_update", "tasks", task_id, None, json.dumps(updates))
    return {"message": "updated"}


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
    await create_operation_log(db, current_user.id, "task_delete", "tasks", task_id)
    return {"message": "deleted"}