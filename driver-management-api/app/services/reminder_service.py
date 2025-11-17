import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models import Driver, DriverCertificate, Vehicle, User
from app.crud import create_operation_log
from app.services.email_service import email_service

logger = logging.getLogger(__name__)

class ReminderService:
    """驾照和证书到期提醒服务"""
    
    def __init__(self):
        self.reminder_days = [30, 15, 7, 3, 1]  # 提前提醒天数
        
    async def check_expiring_licenses(self) -> List[Dict[str, Any]]:
        """检查即将到期的驾照和证书"""
        reminders = []
        
        async with AsyncSessionLocal() as session:
            for days_before in self.reminder_days:
                target_date = datetime.now().date() + timedelta(days=days_before)
                
                # 检查司机证书到期
                stmt = select(DriverCertificate).where(
                    and_(
                        DriverCertificate.expiry_date == target_date,
                        DriverCertificate.status == "valid"
                    )
                )
                result = await session.execute(stmt)
                certificates = result.scalars().all()
                
                for cert in certificates:
                    # 获取司机信息
                    driver_stmt = select(Driver).where(Driver.id == cert.driver_id)
                    driver_result = await session.execute(driver_stmt)
                    driver = driver_result.scalar_one_or_none()
                    
                    if driver:
                        # 获取用户信息
                        user_stmt = select(User).where(User.id == driver.user_id)
                        user_result = await session.execute(user_stmt)
                        user = user_result.scalar_one_or_none()
                        
                        reminder = {
                            "type": "certificate_expiry",
                            "days_before": days_before,
                            "driver_name": driver.name,
                            "driver_phone": driver.phone,
                            "certificate_type": cert.certificate_type,
                            "certificate_number": cert.certificate_number,
                            "expiry_date": cert.expiry_date,
                            "user_email": user.email if user else None,
                            "user_role": user.role if user else None
                        }
                        reminders.append(reminder)
                        
                        # 记录操作日志
                        await create_operation_log(
                            session, 
                            user.id if user else 0,
                            "certificate_expiry_reminder",
                            "driver_certificates",
                            cert.id,
                            None,
                            f"证书即将到期提醒: {cert.certificate_type} - {days_before}天后到期"
                        )
                
                # 检查车辆保险到期
                vehicle_stmt = select(Vehicle).where(
                    and_(
                        Vehicle.insurance_expiry == target_date,
                        Vehicle.status == "active"
                    )
                )
                vehicle_result = await session.execute(vehicle_stmt)
                vehicles = vehicle_result.scalars().all()
                
                for vehicle in vehicles:
                    # 获取当前司机信息
                    if vehicle.current_driver_id:
                        driver_stmt = select(Driver).where(Driver.id == vehicle.current_driver_id)
                        driver_result = await session.execute(driver_stmt)
                        driver = driver_result.scalar_one_or_none()
                        
                        if driver:
                            user_stmt = select(User).where(User.id == driver.user_id)
                            user_result = await session.execute(user_stmt)
                            user = user_result.scalar_one_or_none()
                            
                            reminder = {
                                "type": "insurance_expiry",
                                "days_before": days_before,
                                "vehicle_plate": vehicle.plate_number,
                                "driver_name": driver.name,
                                "driver_phone": driver.phone,
                                "expiry_date": vehicle.insurance_expiry,
                                "user_email": user.email if user else None,
                                "user_role": user.role if user else None
                            }
                            reminders.append(reminder)
                            
                            await create_operation_log(
                                session,
                                user.id if user else 0,
                                "insurance_expiry_reminder",
                                "vehicles",
                                vehicle.id,
                                None,
                                f"车辆保险即将到期提醒: {vehicle.plate_number} - {days_before}天后到期"
                            )
                
                # 检查车辆年检到期
                inspection_stmt = select(Vehicle).where(
                    and_(
                        Vehicle.annual_inspection_date == target_date,
                        Vehicle.status == "active"
                    )
                )
                inspection_result = await session.execute(inspection_stmt)
                vehicles_inspection = inspection_result.scalars().all()
                
                for vehicle in vehicles_inspection:
                    if vehicle.current_driver_id:
                        driver_stmt = select(Driver).where(Driver.id == vehicle.current_driver_id)
                        driver_result = await session.execute(driver_stmt)
                        driver = driver_result.scalar_one_or_none()
                        
                        if driver:
                            user_stmt = select(User).where(User.id == driver.user_id)
                            user_result = await session.execute(user_stmt)
                            user = user_result.scalar_one_or_none()
                            
                            reminder = {
                                "type": "inspection_expiry",
                                "days_before": days_before,
                                "vehicle_plate": vehicle.plate_number,
                                "driver_name": driver.name,
                                "driver_phone": driver.phone,
                                "expiry_date": vehicle.annual_inspection_date,
                                "user_email": user.email if user else None,
                                "user_role": user.role if user else None
                            }
                            reminders.append(reminder)
                            
                            await create_operation_log(
                                session,
                                user.id if user else 0,
                                "inspection_expiry_reminder",
                                "vehicles",
                                vehicle.id,
                                None,
                                f"车辆年检即将到期提醒: {vehicle.plate_number} - {days_before}天后到期"
                            )
                
                await session.commit()
        
        return reminders
    
    async def send_reminders(self, reminders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """发送提醒通知"""
        results = {
            "total": len(reminders),
            "sent": 0,
            "failed": 0,
            "details": []
        }
        
        # 按用户分组发送邮件
        user_reminders = {}
        for reminder in reminders:
            email = reminder.get("user_email")
            if email:
                if email not in user_reminders:
                    user_reminders[email] = []
                user_reminders[email].append(reminder)
        
        # 发送邮件通知
        for email, user_reminder_list in user_reminders.items():
            try:
                success = email_service.send_reminder_email(email, user_reminder_list)
                if success:
                    results["sent"] += len(user_reminder_list)
                    results["details"].append({
                        "email": email,
                        "count": len(user_reminder_list),
                        "status": "sent"
                    })
                else:
                    results["failed"] += len(user_reminder_list)
                    results["details"].append({
                        "email": email,
                        "count": len(user_reminder_list),
                        "status": "failed",
                        "error": "邮件发送失败"
                    })
            except Exception as e:
                logger.error(f"发送邮件提醒失败: {e}")
                results["failed"] += len(user_reminder_list)
                results["details"].append({
                    "email": email,
                    "count": len(user_reminder_list),
                    "status": "failed",
                    "error": str(e)
                })
        
        # 记录没有邮箱的提醒
        no_email_count = len([r for r in reminders if not r.get("user_email")])
        if no_email_count > 0:
            results["details"].append({
                "email": "无邮箱地址",
                "count": no_email_count,
                "status": "skipped",
                "note": "用户未配置邮箱地址"
            })
            logger.info(f"跳过 {no_email_count} 个无邮箱地址的提醒")
        
        return results
    
    async def run_daily_check(self) -> Dict[str, Any]:
        """运行每日检查"""
        logger.info("开始执行每日到期提醒检查")
        
        try:
            # 检查即将到期的项目
            reminders = await self.check_expiring_licenses()
            
            if reminders:
                # 发送提醒
                results = await self.send_reminders(reminders)
                logger.info(f"每日检查完成: 发现 {len(reminders)} 个提醒, 发送成功 {results['sent']} 个")
                return results
            else:
                logger.info("每日检查完成: 未发现即将到期的项目")
                return {"message": "未发现即将到期的项目", "reminders": 0}
                
        except Exception as e:
            logger.error(f"每日检查失败: {e}")
            return {"error": str(e)}

# 全局服务实例
reminder_service = ReminderService()