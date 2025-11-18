from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models import FileAsset, User
from app.crud import create_operation_log
import os
import uuid

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("")
async def list_files(q: str | None = None, related_type: str | None = None, related_id: str | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    stmt = select(FileAsset)
    if q:
        from sqlalchemy import or_
        stmt = stmt.where(or_(FileAsset.name.ilike(f"%{q}%"), FileAsset.mime_type.ilike(f"%{q}%")))
    if related_type:
        stmt = stmt.where(FileAsset.related_type == related_type)
    if related_id:
        stmt = stmt.where(FileAsset.related_id == related_id)
    result = await db.execute(stmt.order_by(FileAsset.created_at.desc()))
    return [f for f, in result.all()]


@router.get("/{file_id}")
async def get_file(file_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(FileAsset).where(FileAsset.id == file_id))
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    return file


@router.post("")
async def upload_file(
    upload: UploadFile = File(...),
    related_type: str | None = Form(None),
    related_id: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ext = os.path.splitext(upload.filename or "")[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(await upload.read())
    stat = os.stat(fpath)
    # 版本控制：同名+关联对象，版本+1
    from sqlalchemy import func
    version = 1
    if related_type and related_id:
        existing = await db.execute(select(func.max(FileAsset.version)).where(
            FileAsset.related_type == related_type,
            FileAsset.related_id == related_id,
            FileAsset.name == (upload.filename or fname)
        ))
        maxv = existing.scalar() or 0
        version = int(maxv) + 1

    asset = FileAsset(
        name=upload.filename or fname,
        mime_type=upload.content_type or "application/octet-stream",
        size=int(stat.st_size),
        path=f"/static/uploads/{fname}",
        uploader_id=current_user.id,
        related_type=related_type,
        related_id=related_id,
        version=version,
    )
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    await create_operation_log(db, current_user.id, "file_upload", "file_assets", asset.id, None, None)
    return asset


@router.delete("/{file_id}")
async def delete_file(file_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(FileAsset).where(FileAsset.id == file_id))
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    # 删除物理文件
    try:
        full = os.path.join(os.getcwd(), file.path.lstrip("/"))
        if os.path.exists(full):
            os.remove(full)
    except Exception:
        pass
    await db.execute(delete(FileAsset).where(FileAsset.id == file_id))
    await db.commit()
    await create_operation_log(db, current_user.id, "file_delete", "file_assets", file_id, None, None)
    return {"message": "文件已删除"}