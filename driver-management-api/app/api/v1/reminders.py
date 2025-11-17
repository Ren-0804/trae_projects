import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.deps import get_db, get_current_user
from app.models import User
from app.services.reminder_service import reminder_service
from app.services.task_manager import task_manager
from app.schemas import ReminderResponse, ReminderSettings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/check", response_model=dict)
async def check_expiring_items(
    days_ahead: int = Query(30, ge=1, le=365, description="提前检查天数"),
    current_user: User = Depends(get_current_user)
):
    """手动检查即将到期的驾照和证书"""
    try:
        # 临时修改提醒天数进行检查
        original_days = reminder_service.reminder_days
        reminder_service.reminder_days = [days_ahead]
        
        reminders = await reminder_service.check_expiring_licenses()
        
        # 恢复原始提醒天数
        reminder_service.reminder_days = original_days
        
        return {
            "code": 20000,
            "message": "检查完成",
            "data": {
                "total_count": len(reminders),
                "reminders": reminders,
                "check_date": datetime.now().isoformat(),
                "days_ahead": days_ahead
            }
        }
    except Exception as e:
        logger.error(f"检查到期项目失败: {e}")
        raise HTTPException(status_code=500, detail=f"检查失败: {str(e)}")

@router.post("/send-reminders", response_model=dict)
async def send_manual_reminders(
    reminder_types: List[str] = Query(["certificate_expiry", "insurance_expiry", "inspection_expiry"]),
    days_ahead: int = Query(7, ge=1, le=365, description="提前提醒天数"),
    current_user: User = Depends(get_current_user)
):
    """手动发送提醒通知"""
    try:
        # 检查即将到期的项目
        original_days = reminder_service.reminder_days
        reminder_service.reminder_days = [days_ahead]
        
        reminders = await reminder_service.check_expiring_licenses()
        
        # 过滤指定类型的提醒
        filtered_reminders = [
            reminder for reminder in reminders 
            if reminder["type"] in reminder_types
        ]
        
        # 恢复原始提醒天数
        reminder_service.reminder_days = original_days
        
        if not filtered_reminders:
            return {
                "code": 20000,
                "message": "未发现指定类型的到期提醒",
                "data": {
                    "total_count": 0,
                    "sent_count": 0,
                    "types": reminder_types,
                    "days_ahead": days_ahead
                }
            }
        
        # 发送提醒
        results = await reminder_service.send_reminders(filtered_reminders)
        
        return {
            "code": 20000,
            "message": "提醒发送完成",
            "data": {
                "total_count": results["total"],
                "sent_count": results["sent"],
                "failed_count": results["failed"],
                "details": results["details"],
                "types": reminder_types,
                "days_ahead": days_ahead
            }
        }
    except Exception as e:
        logger.error(f"发送提醒失败: {e}")
        raise HTTPException(status_code=500, detail=f"发送提醒失败: {str(e)}")

@router.get("/settings", response_model=dict)
async def get_reminder_settings(
    current_user: User = Depends(get_current_user)
):
    """获取提醒设置"""
    return {
        "code": 20000,
        "message": "获取设置成功",
        "data": {
            "reminder_days": reminder_service.reminder_days,
            "enabled": True,
            "notification_methods": ["email", "sms", "push"],  # 支持的通知方式
            "default_days_ahead": 30
        }
    }

@router.put("/settings", response_model=dict)
async def update_reminder_settings(
    settings: ReminderSettings,
    current_user: User = Depends(get_current_user)
):
    """更新提醒设置"""
    try:
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 更新提醒天数
        if settings.reminder_days:
            reminder_service.reminder_days = sorted(settings.reminder_days)
        
        return {
            "code": 20000,
            "message": "设置更新成功",
            "data": {
                "reminder_days": reminder_service.reminder_days,
                "updated_by": current_user.username,
                "updated_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"更新提醒设置失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新设置失败: {str(e)}")

@router.get("/dashboard", response_model=dict)
async def get_reminder_dashboard(
    days_ahead: int = Query(30, ge=1, le=365, description="统计天数"),
    current_user: User = Depends(get_current_user)
):
    """获取提醒仪表板数据"""
    try:
        # 临时设置检查天数
        original_days = reminder_service.reminder_days
        reminder_service.reminder_days = list(range(1, days_ahead + 1))
        
        reminders = await reminder_service.check_expiring_licenses()
        
        # 恢复原始设置
        reminder_service.reminder_days = original_days
        
        # 统计数据
        stats = {
            "certificate_expiry": 0,
            "insurance_expiry": 0,
            "inspection_expiry": 0
        }
        
        timeline = {}
        
        for reminder in reminders:
            reminder_type = reminder["type"]
            days_before = reminder["days_before"]
            
            if reminder_type in stats:
                stats[reminder_type] += 1
            
            # 按时间线分组
            if days_before not in timeline:
                timeline[days_before] = {
                    "certificate_expiry": 0,
                    "insurance_expiry": 0,
                    "inspection_expiry": 0
                }
            
            timeline[days_before][reminder_type] += 1
        
        return {
            "code": 20000,
            "message": "获取仪表板数据成功",
            "data": {
                "total_count": len(reminders),
                "statistics": stats,
                "timeline": timeline,
                "days_ahead": days_ahead,
                "generated_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"获取仪表板数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取数据失败: {str(e)}")

@router.get("/tasks/status", response_model=dict)
async def get_task_status(
    current_user: User = Depends(get_current_user)
):
    """获取后台任务状态"""
    try:
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        status = task_manager.get_job_status()
        
        return {
            "code": 20000,
            "message": "获取任务状态成功",
            "data": status
        }
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取任务状态失败: {str(e)}")

@router.post("/tasks/trigger", response_model=dict)
async def trigger_task_check(
    task_type: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
    current_user: User = Depends(get_current_user)
):
    """手动触发后台任务"""
    try:
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(status_code=403, detail="权限不足")
        
        if task_type == "daily":
            result = await reminder_service.run_daily_check()
        elif task_type == "weekly":
            await task_manager.weekly_reminder_check()
            result = {"message": "每周提醒检查已触发"}
        elif task_type == "monthly":
            await task_manager.monthly_reminder_check()
            result = {"message": "每月提醒检查已触发"}
        else:
            raise HTTPException(status_code=400, detail="无效的任务类型")
        
        return {
            "code": 20000,
            "message": "任务触发成功",
            "data": {
                "task_type": task_type,
                "triggered_at": datetime.now().isoformat(),
                "result": result
            }
        }
    except Exception as e:
        logger.error(f"触发任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"触发任务失败: {str(e)}")