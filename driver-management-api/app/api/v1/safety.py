from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import logger
from app.models import User, GPSRecord, DrivingBehavior, EmergencyAlert, Driver, Vehicle
from app.schemas import (
    GPSRecordCreate, GPSRecordResponse,
    DrivingBehaviorCreate, DrivingBehaviorUpdate, DrivingBehaviorResponse,
    EmergencyAlertCreate, EmergencyAlertUpdate, EmergencyAlertResponse
)
from app.crud import create_operation_log

router = APIRouter(prefix="/safety", tags=["safety"])


# GPS轨迹管理
@router.post("/gps-records", response_model=GPSRecordResponse)
async def create_gps_record(
    gps_record: GPSRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建GPS记录"""
    try:
        # 验证车辆是否存在
        vehicle = db.query(Vehicle).filter(Vehicle.id == gps_record.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        # 验证司机是否存在（如果指定了司机）
        if gps_record.driver_id:
            driver = db.query(Driver).filter(Driver.id == gps_record.driver_id).first()
            if not driver:
                raise HTTPException(status_code=404, detail="司机不存在")
        
        db_gps_record = GPSRecord(**gps_record.dict())
        db.add(db_gps_record)
        db.commit()
        db.refresh(db_gps_record)
        
        logger.info(f"用户 {current_user.username} 创建了GPS记录，车辆 {vehicle.plate_number}")
        return db_gps_record
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建GPS记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建GPS记录失败")


@router.get("/gps-records", response_model=List[GPSRecordResponse])
async def get_gps_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vehicle_id: Optional[int] = Query(None),
    driver_id: Optional[int] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取GPS记录列表"""
    try:
        query = db.query(GPSRecord)
        
        if vehicle_id:
            query = query.filter(GPSRecord.vehicle_id == vehicle_id)
        if driver_id:
            query = query.filter(GPSRecord.driver_id == driver_id)
        if start_time:
            query = query.filter(GPSRecord.timestamp >= start_time)
        if end_time:
            query = query.filter(GPSRecord.timestamp <= end_time)
            
        gps_records = query.order_by(GPSRecord.timestamp.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"用户 {current_user.username} 获取了 {len(gps_records)} 条GPS记录")
        return gps_records
        
    except Exception as e:
        logger.error(f"获取GPS记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取GPS记录失败")


@router.get("/vehicles/{vehicle_id}/track")
async def get_vehicle_track(
    vehicle_id: int,
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取车辆轨迹"""
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
            
        if start_time >= end_time:
            raise HTTPException(status_code=400, detail="结束时间必须晚于开始时间")
            
        # 获取轨迹点
        gps_records = db.query(GPSRecord).filter(
            GPSRecord.vehicle_id == vehicle_id,
            GPSRecord.timestamp >= start_time,
            GPSRecord.timestamp <= end_time
        ).order_by(GPSRecord.timestamp.asc()).all()
        
        # 计算统计信息
        total_distance = 0.0
        max_speed = 0.0
        avg_speed = 0.0
        idle_time = 0
        
        if gps_records:
            speeds = [float(record.speed) for record in gps_records if record.speed]
            if speeds:
                max_speed = max(speeds)
                avg_speed = sum(speeds) / len(speeds)
            
            # 计算距离（简化计算，实际应该使用更精确的算法）
            for i in range(1, len(gps_records)):
                prev_record = gps_records[i-1]
                curr_record = gps_records[i]
                
                # 计算两点间距离（这里使用简化的距离计算）
                distance = calculate_distance(
                    float(prev_record.latitude), float(prev_record.longitude),
                    float(curr_record.latitude), float(curr_record.longitude)
                )
                total_distance += distance
                
                # 计算怠速时间
                if curr_record.status == "idle":
                    time_diff = (curr_record.timestamp - prev_record.timestamp).total_seconds()
                    idle_time += time_diff
        
        result = {
            "vehicle_id": vehicle_id,
            "plate_number": vehicle.plate_number,
            "start_time": start_time,
            "end_time": end_time,
            "total_points": len(gps_records),
            "total_distance": round(total_distance, 2),
            "max_speed": round(max_speed, 2),
            "avg_speed": round(avg_speed, 2),
            "idle_time": int(idle_time),
            "track": [
                {
                    "latitude": float(record.latitude),
                    "longitude": float(record.longitude),
                    "speed": float(record.speed) if record.speed else 0,
                    "timestamp": record.timestamp,
                    "address": record.address,
                    "status": record.status
                }
                for record in gps_records
            ]
        }
        
        logger.info(f"用户 {current_user.username} 获取了车辆 {vehicle.plate_number} 的轨迹数据")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取车辆轨迹失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取车辆轨迹失败")


# 驾驶行为管理
@router.post("/driving-behaviors", response_model=DrivingBehaviorResponse)
async def create_driving_behavior(
    behavior: DrivingBehaviorCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建驾驶行为记录"""
    try:
        # 验证司机是否存在
        driver = db.query(Driver).filter(Driver.id == behavior.driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        # 验证车辆是否存在（如果指定了车辆）
        if behavior.vehicle_id:
            vehicle = db.query(Vehicle).filter(Vehicle.id == behavior.vehicle_id).first()
            if not vehicle:
                raise HTTPException(status_code=404, detail="车辆不存在")
        
        db_behavior = DrivingBehavior(**behavior.dict())
        db.add(db_behavior)
        db.commit()
        db.refresh(db_behavior)
        
        # 后台处理异常行为预警
        if behavior.severity == "high":
            background_tasks.add_task(process_high_risk_behavior, db_behavior.id, current_user.id)
        
        logger.info(f"用户 {current_user.username} 创建了驾驶行为记录，司机 {driver.name}")
        return db_behavior
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建驾驶行为记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建驾驶行为记录失败")


@router.get("/driving-behaviors", response_model=List[DrivingBehaviorResponse])
async def get_driving_behaviors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    driver_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    behavior_type: Optional[str] = Query(None, pattern="^(harsh_braking|speeding|sharp_turn)$"),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
    processed: Optional[bool] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取驾驶行为记录列表"""
    try:
        query = db.query(DrivingBehavior)
        
        if driver_id:
            query = query.filter(DrivingBehavior.driver_id == driver_id)
        if vehicle_id:
            query = query.filter(DrivingBehavior.vehicle_id == vehicle_id)
        if behavior_type:
            query = query.filter(DrivingBehavior.behavior_type == behavior_type)
        if severity:
            query = query.filter(DrivingBehavior.severity == severity)
        if processed is not None:
            query = query.filter(DrivingBehavior.processed == processed)
        if start_time:
            query = query.filter(DrivingBehavior.timestamp >= start_time)
        if end_time:
            query = query.filter(DrivingBehavior.timestamp <= end_time)
            
        behaviors = query.order_by(DrivingBehavior.timestamp.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"用户 {current_user.username} 获取了 {len(behaviors)} 条驾驶行为记录")
        return behaviors
        
    except Exception as e:
        logger.error(f"获取驾驶行为记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取驾驶行为记录失败")


@router.put("/driving-behaviors/{behavior_id}", response_model=DrivingBehaviorResponse)
async def update_driving_behavior(
    behavior_id: int,
    behavior_update: DrivingBehaviorUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新驾驶行为记录"""
    try:
        behavior = db.query(DrivingBehavior).filter(DrivingBehavior.id == behavior_id).first()
        if not behavior:
            raise HTTPException(status_code=404, detail="驾驶行为记录不存在")
        
        # 记录旧数据
        old_data = behavior.json()
        
        # 更新字段
        behavior.processed = behavior_update.processed
        db.commit()
        db.refresh(behavior)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="update",
            table_name="driving_behaviors",
            record_id=behavior_id,
            old_data=old_data,
            new_data=behavior.json()
        )
        
        logger.info(f"用户 {current_user.username} 更新了驾驶行为记录 {behavior_id}")
        return behavior
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新驾驶行为记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新驾驶行为记录失败")


@router.get("/driving-behaviors/summary")
async def get_driving_behavior_summary(
    driver_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取驾驶行为统计摘要"""
    try:
        query = db.query(DrivingBehavior)
        
        if driver_id:
            query = query.filter(DrivingBehavior.driver_id == driver_id)
        if vehicle_id:
            query = query.filter(DrivingBehavior.vehicle_id == vehicle_id)
        if start_date:
            query = query.filter(DrivingBehavior.timestamp >= start_date)
        if end_date:
            query = query.filter(DrivingBehavior.timestamp <= end_date)
            
        behaviors = query.all()
        
        # 统计各种行为
        summary = {
            "total_behaviors": len(behaviors),
            "by_type": {
                "harsh_braking": 0,
                "speeding": 0,
                "sharp_turn": 0
            },
            "by_severity": {
                "low": 0,
                "medium": 0,
                "high": 0
            },
            "processed_count": 0,
            "unprocessed_count": 0
        }
        
        for behavior in behaviors:
            summary["by_type"][behavior.behavior_type] += 1
            summary["by_severity"][behavior.severity] += 1
            
            if behavior.processed:
                summary["processed_count"] += 1
            else:
                summary["unprocessed_count"] += 1
        
        # 计算高风险行为占比
        total_high_risk = summary["by_severity"]["high"]
        summary["high_risk_percentage"] = round((total_high_risk / len(behaviors) * 100), 2) if behaviors else 0
        
        logger.info(f"用户 {current_user.username} 获取了驾驶行为统计摘要")
        return summary
        
    except Exception as e:
        logger.error(f"获取驾驶行为统计摘要失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取驾驶行为统计摘要失败")


# 紧急警报管理
@router.post("/emergency-alerts", response_model=EmergencyAlertResponse)
async def create_emergency_alert(
    alert: EmergencyAlertCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建紧急警报"""
    try:
        # 验证司机是否存在
        driver = db.query(Driver).filter(Driver.id == alert.driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="司机不存在")
            
        # 验证车辆是否存在（如果指定了车辆）
        if alert.vehicle_id:
            vehicle = db.query(Vehicle).filter(Vehicle.id == alert.vehicle_id).first()
            if not vehicle:
                raise HTTPException(status_code=404, detail="车辆不存在")
        
        db_alert = EmergencyAlert(**alert.dict())
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        
        # 后台处理紧急警报通知
        background_tasks.add_task(process_emergency_alert, db_alert.id, current_user.id)
        
        logger.warning(f"用户 {current_user.username} 创建了紧急警报，司机 {driver.name}，类型 {alert.alert_type}")
        return db_alert
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建紧急警报失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建紧急警报失败")


@router.get("/emergency-alerts", response_model=List[EmergencyAlertResponse])
async def get_emergency_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    driver_id: Optional[int] = Query(None),
    vehicle_id: Optional[int] = Query(None),
    alert_type: Optional[str] = Query(None, pattern="^(accident|medical|security)$"),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    status: Optional[str] = Query(None, pattern="^(active|responded|resolved)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取紧急警报列表"""
    try:
        query = db.query(EmergencyAlert)
        
        if driver_id:
            query = query.filter(EmergencyAlert.driver_id == driver_id)
        if vehicle_id:
            query = query.filter(EmergencyAlert.vehicle_id == vehicle_id)
        if alert_type:
            query = query.filter(EmergencyAlert.alert_type == alert_type)
        if severity:
            query = query.filter(EmergencyAlert.severity == severity)
        if status:
            query = query.filter(EmergencyAlert.status == status)
            
        alerts = query.order_by(EmergencyAlert.created_at.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"用户 {current_user.username} 获取了 {len(alerts)} 条紧急警报")
        return alerts
        
    except Exception as e:
        logger.error(f"获取紧急警报失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取紧急警报失败")


@router.put("/emergency-alerts/{alert_id}", response_model=EmergencyAlertResponse)
async def update_emergency_alert(
    alert_id: int,
    alert_update: EmergencyAlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新紧急警报"""
    try:
        alert = db.query(EmergencyAlert).filter(EmergencyAlert.id == alert_id).first()
        if not alert:
            raise HTTPException(status_code=404, detail="紧急警报不存在")
        
        # 记录旧数据
        old_data = alert.json()
        
        # 更新字段
        alert.status = alert_update.status
        alert.responded_by = alert_update.responded_by
        alert.response_time = alert_update.response_time or datetime.now()
        alert.updated_at = datetime.now()
        
        db.commit()
        db.refresh(alert)
        
        # 记录操作日志
        create_operation_log(
            db=db,
            user_id=current_user.id,
            operation_type="update",
            table_name="emergency_alerts",
            record_id=alert_id,
            old_data=old_data,
            new_data=alert.json()
        )
        
        logger.info(f"用户 {current_user.username} 更新了紧急警报 {alert_id}，状态 {alert_update.status}")
        return alert
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新紧急警报失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新紧急警报失败")


@router.get("/emergency-alerts/active-summary")
async def get_active_emergency_alerts_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取活跃紧急警报摘要"""
    try:
        active_alerts = db.query(EmergencyAlert).filter(
            EmergencyAlert.status == "active"
        ).all()
        
        summary = {
            "total_active_alerts": len(active_alerts),
            "by_type": {
                "accident": 0,
                "medical": 0,
                "security": 0
            },
            "by_severity": {
                "low": 0,
                "medium": 0,
                "high": 0,
                "critical": 0
            },
            "latest_alerts": []
        }
        
        for alert in active_alerts:
            summary["by_type"][alert.alert_type] += 1
            summary["by_severity"][alert.severity] += 1
            
            # 只保留最新的5条警报
            if len(summary["latest_alerts"]) < 5:
                summary["latest_alerts"].append({
                    "id": alert.id,
                    "driver_name": alert.driver.name,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "description": alert.description,
                    "created_at": alert.created_at,
                    "latitude": float(alert.latitude) if alert.latitude else None,
                    "longitude": float(alert.longitude) if alert.longitude else None
                })
        
        # 按创建时间排序
        summary["latest_alerts"].sort(key=lambda x: x["created_at"], reverse=True)
        
        logger.info(f"用户 {current_user.username} 获取了活跃紧急警报摘要")
        return summary
        
    except Exception as e:
        logger.error(f"获取活跃紧急警报摘要失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取活跃紧急警报摘要失败")


# 辅助函数
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """计算两点间距离（简化版，单位：公里）"""
    import math
    
    # 简化的距离计算，实际应该使用更精确的算法如Haversine公式
    lat_diff = abs(lat2 - lat1)
    lon_diff = abs(lon2 - lon1)
    
    # 粗略估算：1度纬度约111公里，1度经度在赤道约111公里
    lat_km = lat_diff * 111
    lon_km = lon_diff * 111 * math.cos(math.radians((lat1 + lat2) / 2))
    
    return math.sqrt(lat_km**2 + lon_km**2)


async def process_high_risk_behavior(behavior_id: int, user_id: int):
    """处理高风险驾驶行为"""
    # 这里可以实现发送通知、记录日志等逻辑
    logger.warning(f"高风险驾驶行为检测到，行为ID: {behavior_id}，处理用户ID: {user_id}")


async def process_emergency_alert(alert_id: int, user_id: int):
    """处理紧急警报"""
    # 这里可以实现发送通知、记录日志等逻辑
    logger.critical(f"紧急警报创建，警报ID: {alert_id}，创建用户ID: {user_id}")


# 新增用于前端仪表板的API端点
@router.get("/stats")
async def get_safety_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取安全统计信息"""
    try:
        # 统计在线司机（假设有GPS记录在最近30分钟内即为在线）
        thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
        online_drivers = db.query(Driver).join(GPSRecord).filter(
            GPSRecord.timestamp >= thirty_minutes_ago
        ).distinct().count()
        
        # 统计活跃车辆（假设有GPS记录在最近30分钟内即为活跃）
        active_vehicles = db.query(Vehicle).join(GPSRecord).filter(
            GPSRecord.timestamp >= thirty_minutes_ago
        ).distinct().count()
        
        # 统计今日预警
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_alerts = db.query(DrivingBehavior).filter(
            DrivingBehavior.timestamp >= today_start
        ).count()
        
        # 统计紧急报警
        emergency_alerts = db.query(EmergencyAlert).filter(
            EmergencyAlert.status == "active"
        ).count()
        
        stats = {
            "online_drivers": online_drivers,
            "active_vehicles": active_vehicles,
            "today_alerts": today_alerts,
            "emergency_alerts": emergency_alerts
        }
        
        logger.info(f"用户 {current_user.username} 获取了安全统计信息")
        return stats
        
    except Exception as e:
        logger.error(f"获取安全统计信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取安全统计信息失败")


@router.get("/alerts/recent")
async def get_recent_alerts(
    limit: int = Query(10, ge=1, le=100),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    status: Optional[str] = Query(None, pattern="^(active|acknowledged|resolved)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取最近预警"""
    try:
        query = db.query(DrivingBehavior).join(Driver)
        
        if severity:
            query = query.filter(DrivingBehavior.severity == severity)
        if status:
            if status == "active":
                query = query.filter(DrivingBehavior.processed == False)
            elif status == "acknowledged":
                query = query.filter(DrivingBehavior.processed == True)
        
        alerts = query.order_by(DrivingBehavior.timestamp.desc()).limit(limit).all()
        
        result = {
            "data": [
                {
                    "id": alert.id,
                    "alert_type": alert.behavior_type,
                    "severity": alert.severity,
                    "status": "active" if not alert.processed else "acknowledged",
                    "description": f"{alert.behavior_type} - {alert.severity} severity",
                    "created_at": alert.timestamp.isoformat(),
                    "driver": {
                        "id": alert.driver.id,
                        "name": alert.driver.name
                    }
                }
                for alert in alerts
            ],
            "total": len(alerts)
        }
        
        logger.info(f"用户 {current_user.username} 获取了最近 {len(alerts)} 条预警")
        return result
        
    except Exception as e:
        logger.error(f"获取最近预警失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取最近预警失败")


@router.get("/alerts")
async def get_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    status: Optional[str] = Query(None, pattern="^(active|acknowledged|resolved)$"),
    driver_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取预警列表"""
    try:
        query = db.query(DrivingBehavior).join(Driver)
        
        if severity:
            query = query.filter(DrivingBehavior.severity == severity)
        if status:
            if status == "active":
                query = query.filter(DrivingBehavior.processed == False)
            elif status == "acknowledged":
                query = query.filter(DrivingBehavior.processed == True)
        if driver_id:
            query = query.filter(DrivingBehavior.driver_id == driver_id)
        
        total = query.count()
        alerts = query.order_by(DrivingBehavior.timestamp.desc()).offset((page-1)*page_size).limit(page_size).all()
        
        result = {
            "data": [
                {
                    "id": alert.id,
                    "alert_type": alert.behavior_type,
                    "severity": alert.severity,
                    "status": "active" if not alert.processed else "acknowledged",
                    "description": f"{alert.behavior_type} - {alert.severity} severity",
                    "created_at": alert.timestamp.isoformat(),
                    "driver": {
                        "id": alert.driver.id,
                        "name": alert.driver.name
                    }
                }
                for alert in alerts
            ],
            "total": total
        }
        
        logger.info(f"用户 {current_user.username} 获取了预警列表，共 {total} 条")
        return result
        
    except Exception as e:
        logger.error(f"获取预警列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取预警列表失败")


@router.put("/alerts/{alert_id}/process")
async def process_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """处理预警"""
    try:
        alert = db.query(DrivingBehavior).filter(DrivingBehavior.id == alert_id).first()
        if not alert:
            raise HTTPException(status_code=404, detail="预警不存在")
        
        alert.processed = True
        db.commit()
        
        logger.info(f"用户 {current_user.username} 处理了预警 {alert_id}")
        return {"message": "预警处理成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"处理预警失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理预警失败")


@router.get("/emergency-alerts/stats")
async def get_emergency_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取紧急报警统计"""
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        today_emergency = db.query(EmergencyAlert).filter(
            EmergencyAlert.created_at >= today_start
        ).count()
        
        pending_emergency = db.query(EmergencyAlert).filter(
            EmergencyAlert.status == "active"
        ).count()
        
        resolved_emergency = db.query(EmergencyAlert).filter(
            EmergencyAlert.status == "resolved"
        ).count()
        
        stats = {
            "today_emergency": today_emergency,
            "pending_emergency": pending_emergency,
            "resolved_emergency": resolved_emergency
        }
        
        logger.info(f"用户 {current_user.username} 获取了紧急报警统计")
        return stats
        
    except Exception as e:
        logger.error(f"获取紧急报警统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取紧急报警统计失败")


@router.put("/emergency-alerts/{alert_id}/process")
async def process_emergency_alert_endpoint(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """处理紧急报警"""
    try:
        alert = db.query(EmergencyAlert).filter(EmergencyAlert.id == alert_id).first()
        if not alert:
            raise HTTPException(status_code=404, detail="紧急报警不存在")
        
        alert.status = "responded"
        alert.responded_by = current_user.id
        alert.response_time = datetime.now()
        db.commit()
        
        logger.info(f"用户 {current_user.username} 处理了紧急报警 {alert_id}")
        return {"message": "紧急报警处理成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"处理紧急报警失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理紧急报警失败")