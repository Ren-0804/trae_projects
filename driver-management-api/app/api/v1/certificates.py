from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User, Driver, DriverCertificate
from app.schemas import (
    DriverCertificateCreate, DriverCertificateUpdate, DriverCertificateResponse
)
from app.crud import create_operation_log

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/", response_model=List[DriverCertificateResponse])
async def get_certificates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    driver_id: Optional[int] = Query(None),
    certificate_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None, pattern="^(valid|expired|suspended)$"),
    expiring_soon: bool = Query(False),
    days_ahead: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取证书列表"""
    try:
        query = db.query(DriverCertificate)
        
        if driver_id:
            query = query.filter(DriverCertificate.driver_id == driver_id)
        if certificate_type:
            query = query.filter(DriverCertificate.certificate_type == certificate_type)
        if status:
            query = query.filter(DriverCertificate.status == status)
            
        if expiring_soon:
            today = datetime.now().date()
            future_date = today + timedelta(days=days_ahead)
            query = query.filter(
                DriverCertificate.expiry_date >= today,
                DriverCertificate.expiry_date <= future_date
            )
            
        certificates = query.order_by(DriverCertificate.expiry_date.asc()).offset(skip).limit(limit).all()
        
        logger.info(f"用户 {current_user.username} 获取了 {len(certificates)} 条证书记录")
        return certificates
        
    except Exception as e:
        logger.error(f"获取证书列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取证书列表失败")


@router.post("/", response_model=DriverCertificateResponse)
async def create_certificate(
    certificate: DriverCertificateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建证书"""
    try:
        # 验证司机是否存在
        driver = db.query(Driver).filter(Driver.id == certificate.driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        # 检查证书号是否已存在
        existing = db.query(DriverCertificate).filter(
            DriverCertificate.certificate_number == certificate.certificate_number
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="证书号已存在")
        
        db_certificate = DriverCertificate(**certificate.dict())
        db.add(db_certificate)
        db.commit()
        db.refresh(db_certificate)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="create",
            table_name="driver_certificates",
            record_id=db_certificate.id,
            old_data=None,
            new_data=certificate.json()
        )
        
        logger.info(f"用户 {current_user.username} 为司机 {driver.name} 创建了证书 {certificate.certificate_type}")
        return db_certificate
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建证书失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建证书失败")


@router.get("/{certificate_id}", response_model=DriverCertificateResponse)
async def get_certificate(
    certificate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取证书详情"""
    try:
        certificate = db.query(DriverCertificate).filter(DriverCertificate.id == certificate_id).first()
        if not certificate:
            raise HTTPException(status_code=404, detail="证书不存在")
            
        logger.info(f"用户 {current_user.username} 查看了证书 {certificate_id}")
        return certificate
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取证书详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取证书详情失败")


@router.put("/{certificate_id}", response_model=DriverCertificateResponse)
async def update_certificate(
    certificate_id: int,
    certificate_update: DriverCertificateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新证书"""
    try:
        certificate = db.query(DriverCertificate).filter(DriverCertificate.id == certificate_id).first()
        if not certificate:
            raise HTTPException(status_code=404, detail="证书不存在")
            
        # 检查证书号是否已存在（如果更新证书号）
        if certificate_update.certificate_number and certificate_update.certificate_number != certificate.certificate_number:
            existing = db.query(DriverCertificate).filter(
                DriverCertificate.certificate_number == certificate_update.certificate_number,
                DriverCertificate.id != certificate_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="证书号已存在")
        
        # 记录旧数据
        old_data = certificate.json()
        
        # 更新字段
        update_data = certificate_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(certificate, field, value)
            
        certificate.updated_at = datetime.now()
        db.commit()
        db.refresh(certificate)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="update",
            table_name="driver_certificates",
            record_id=certificate_id,
            old_data=old_data,
            new_data=certificate.json()
        )
        
        logger.info(f"用户 {current_user.username} 更新了证书 {certificate_id}")
        return certificate
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新证书失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新证书失败")


@router.delete("/{certificate_id}")
async def delete_certificate(
    certificate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除证书"""
    try:
        certificate = db.query(DriverCertificate).filter(DriverCertificate.id == certificate_id).first()
        if not certificate:
            raise HTTPException(status_code=404, detail="证书不存在")
            
        # 记录证书信息用于日志
        certificate_data = certificate.json()
        
        db.delete(certificate)
        db.commit()
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="delete",
            table_name="driver_certificates",
            record_id=certificate_id,
            old_data=certificate_data,
            new_data=None
        )
        
        logger.info(f"用户 {current_user.username} 删除了证书 {certificate_id}")
        return {"message": "证书删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除证书失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除证书失败")


@router.get("/expiring-soon")
async def get_expiring_certificates(
    days_ahead: int = Query(30, ge=1, le=365),
    certificate_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取即将到期的证书"""
    try:
        today = datetime.now().date()
        future_date = today + timedelta(days=days_ahead)
        
        query = db.query(DriverCertificate).filter(
            DriverCertificate.expiry_date >= today,
            DriverCertificate.expiry_date <= future_date,
            DriverCertificate.status == "valid"
        )
        
        if certificate_type:
            query = query.filter(DriverCertificate.certificate_type == certificate_type)
            
        certificates = query.order_by(DriverCertificate.expiry_date.asc()).all()
        
        result = []
        for certificate in certificates:
            days_until = (certificate.expiry_date.date() - today).days
            result.append({
                "certificate_id": certificate.id,
                "driver_id": certificate.driver_id,
                "driver_name": certificate.driver.name,
                "certificate_type": certificate.certificate_type,
                "certificate_number": certificate.certificate_number,
                "expiry_date": certificate.expiry_date,
                "days_until_expiry": days_until,
                "urgency": "high" if days_until <= 7 else "medium" if days_until <= 14 else "low"
            })
        
        logger.info(f"用户 {current_user.username} 获取了 {len(result)} 条即将到期的证书提醒")
        return result
        
    except Exception as e:
        logger.error(f"获取证书到期提醒失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取证书到期提醒失败")


@router.post("/{certificate_id}/renew")
async def renew_certificate(
    certificate_id: int,
    new_expiry_date: datetime = Query(...),
    new_certificate_number: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """续期证书"""
    try:
        certificate = db.query(DriverCertificate).filter(DriverCertificate.id == certificate_id).first()
        if not certificate:
            raise HTTPException(status_code=404, detail="证书不存在")
            
        # 记录旧数据
        old_data = certificate.json()
        
        # 更新证书信息
        certificate.expiry_date = new_expiry_date
        certificate.status = "valid"
        if new_certificate_number:
            certificate.certificate_number = new_certificate_number
            
        certificate.updated_at = datetime.now()
        db.commit()
        db.refresh(certificate)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="renew",
            table_name="driver_certificates",
            record_id=certificate_id,
            old_data=old_data,
            new_data=certificate.json()
        )
        
        logger.info(f"用户 {current_user.username} 续期了证书 {certificate_id}")
        return certificate
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"续期证书失败: {str(e)}")
        raise HTTPException(status_code=500, detail="续期证书失败")


@router.post("/{certificate_id}/upload-file")
async def upload_certificate_file(
    certificate_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传证书文件"""
    try:
        certificate = db.query(DriverCertificate).filter(DriverCertificate.id == certificate_id).first()
        if not certificate:
            raise HTTPException(status_code=404, detail="证书不存在")
            
        # 验证文件类型
        allowed_types = ["image/jpeg", "image/png", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="不支持的文件类型")
            
        # 验证文件大小 (最大 10MB)
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
            
        # 这里应该实现文件上传逻辑，保存到文件系统或云存储
        # 为了演示，我们假设文件已保存并返回一个路径
        file_path = f"/uploads/certificates/{certificate_id}/{file.filename}"
        
        # 记录旧数据
        old_data = certificate.json()
        
        # 更新证书文件路径
        certificate.file_path = file_path
        certificate.updated_at = datetime.now()
        db.commit()
        db.refresh(certificate)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="upload_file",
            table_name="driver_certificates",
            record_id=certificate_id,
            old_data=old_data,
            new_data=certificate.json()
        )
        
        logger.info(f"用户 {current_user.username} 上传了证书 {certificate_id} 的文件")
        return {
            "message": "文件上传成功",
            "file_path": file_path,
            "file_name": file.filename,
            "file_size": len(contents),
            "content_type": file.content_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"上传证书文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail="上传证书文件失败")


@router.get("/drivers/{driver_id}/summary")
async def get_driver_certificates_summary(
    driver_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取司机证书概览"""
    try:
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        certificates = db.query(DriverCertificate).filter(
            DriverCertificate.driver_id == driver_id
        ).all()
        
        today = datetime.now().date()
        summary = {
            "driver_id": driver_id,
            "driver_name": driver.name,
            "total_certificates": len(certificates),
            "valid_certificates": 0,
            "expired_certificates": 0,
            "expiring_soon": 0,
            "certificates_by_type": {},
            "urgent_renewals": []
        }
        
        for certificate in certificates:
            cert_type = certificate.certificate_type
            if cert_type not in summary["certificates_by_type"]:
                summary["certificates_by_type"][cert_type] = {
                    "total": 0,
                    "valid": 0,
                    "expired": 0,
                    "expiring_soon": 0
                }
            
            summary["certificates_by_type"][cert_type]["total"] += 1
            
            days_until = (certificate.expiry_date.date() - today).days
            
            if certificate.status == "valid":
                summary["valid_certificates"] += 1
                summary["certificates_by_type"][cert_type]["valid"] += 1
                
                if days_until <= 30:
                    summary["expiring_soon"] += 1
                    summary["certificates_by_type"][cert_type]["expiring_soon"] += 1
                    
                    if days_until <= 7:
                        summary["urgent_renewals"].append({
                            "certificate_id": certificate.id,
                            "certificate_type": certificate.certificate_type,
                            "certificate_number": certificate.certificate_number,
                            "expiry_date": certificate.expiry_date,
                            "days_until_expiry": days_until
                        })
            else:
                summary["expired_certificates"] += 1
                summary["certificates_by_type"][cert_type]["expired"] += 1
        
        logger.info(f"用户 {current_user.username} 获取了司机 {driver.name} 的证书概览")
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取司机证书概览失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取司机证书概览失败")