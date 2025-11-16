import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException

from app.core.config import settings


async def save_upload_file(file: UploadFile, upload_dir: str) -> str:
    """保存上传文件"""
    # 验证文件类型
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    # 验证文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制")
    
    # 生成唯一文件名
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 创建上传目录
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # 保存文件
    file_path = upload_path / unique_filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return str(file_path)


def delete_file(file_path: str) -> bool:
    """删除文件"""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception:
        return False