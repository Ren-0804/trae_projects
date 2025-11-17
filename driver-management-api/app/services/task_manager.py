import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.reminder_service import reminder_service

logger = logging.getLogger(__name__)

class BackgroundTaskManager:
    """后台任务管理器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        
    def start(self):
        """启动后台任务调度器"""
        if self.is_running:
            logger.warning("后台任务调度器已在运行中")
            return
            
        try:
            # 添加每日提醒检查任务 (每天上午9点执行)
            self.scheduler.add_job(
                self.daily_reminder_check,
                trigger=CronTrigger(hour=9, minute=0),
                id="daily_reminder_check",
                name="每日到期提醒检查",
                replace_existing=True
            )
            
            # 添加每周提醒检查任务 (每周一上午10点执行)
            self.scheduler.add_job(
                self.weekly_reminder_check,
                trigger=CronTrigger(day_of_week=0, hour=10, minute=0),
                id="weekly_reminder_check",
                name="每周到期提醒检查",
                replace_existing=True
            )
            
            # 添加每月提醒检查任务 (每月1号上午8点执行)
            self.scheduler.add_job(
                self.monthly_reminder_check,
                trigger=CronTrigger(day=1, hour=8, minute=0),
                id="monthly_reminder_check",
                name="每月到期提醒检查",
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            logger.info("后台任务调度器启动成功")
            
        except Exception as e:
            logger.error(f"启动后台任务调度器失败: {e}")
            raise
    
    def stop(self):
        """停止后台任务调度器"""
        if not self.is_running:
            logger.warning("后台任务调度器未运行")
            return
            
        try:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("后台任务调度器已停止")
        except Exception as e:
            logger.error(f"停止后台任务调度器失败: {e}")
    
    async def daily_reminder_check(self):
        """每日提醒检查任务"""
        try:
            logger.info("开始执行每日提醒检查任务")
            result = await reminder_service.run_daily_check()
            logger.info(f"每日提醒检查任务完成: {result}")
        except Exception as e:
            logger.error(f"每日提醒检查任务失败: {e}")
    
    async def weekly_reminder_check(self):
        """每周提醒检查任务"""
        try:
            logger.info("开始执行每周提醒检查任务")
            # 设置更长的提醒周期
            original_days = reminder_service.reminder_days
            reminder_service.reminder_days = [60, 45, 30, 15, 7, 3, 1]
            
            result = await reminder_service.run_daily_check()
            
            # 恢复原始设置
            reminder_service.reminder_days = original_days
            logger.info(f"每周提醒检查任务完成: {result}")
        except Exception as e:
            logger.error(f"每周提醒检查任务失败: {e}")
    
    async def monthly_reminder_check(self):
        """每月提醒检查任务"""
        try:
            logger.info("开始执行每月提醒检查任务")
            # 设置更长的提醒周期
            original_days = reminder_service.reminder_days
            reminder_service.reminder_days = [90, 60, 45, 30, 15, 7, 3, 1]
            
            result = await reminder_service.run_daily_check()
            
            # 恢复原始设置
            reminder_service.reminder_days = original_days
            logger.info(f"每月提醒检查任务完成: {result}")
        except Exception as e:
            logger.error(f"每月提醒检查任务失败: {e}")
    
    def get_job_status(self):
        """获取任务状态"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        
        return {
            "is_running": self.is_running,
            "job_count": len(jobs),
            "jobs": jobs
        }

# 全局任务管理器实例
task_manager = BackgroundTaskManager()