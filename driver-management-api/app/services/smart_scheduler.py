from datetime import datetime, timedelta, time
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.models import Driver, Vehicle, Schedule, VehicleAssignment
from app.core.logging import logger
import json

class SmartSchedulerService:
    """智能排班服务"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def generate_optimal_schedule(
        self,
        schedule_date: datetime,
        shift_start: time,
        shift_end: time,
        task_type: str,
        required_drivers: int = 1,
        preferences: Optional[Dict] = None
    ) -> List[Dict]:
        """
        生成最优排班方案
        
        Args:
            schedule_date: 排班日期
            shift_start: 班次开始时间
            shift_end: 班次结束时间
            task_type: 任务类型
            required_drivers: 需要的司机数量
            preferences: 偏好设置
            
        Returns:
            最优排班方案列表
        """
        try:
            # 获取可用司机
            available_drivers = self._get_available_drivers(schedule_date, shift_start, shift_end)
            
            # 获取可用车辆
            available_vehicles = self._get_available_vehicles(schedule_date, shift_start, shift_end)
            
            # 计算司机评分
            driver_scores = self._calculate_driver_scores(available_drivers, schedule_date, preferences)
            
            # 计算车辆评分
            vehicle_scores = self._calculate_vehicle_scores(available_vehicles, task_type)
            
            # 生成排班方案
            schedules = self._generate_schedules(
                driver_scores, vehicle_scores, schedule_date, shift_start, shift_end, task_type, required_drivers
            )
            
            logger.info(f"生成最优排班方案成功，找到 {len(schedules)} 个方案")
            return schedules
            
        except Exception as e:
            logger.error(f"生成最优排班方案失败: {str(e)}")
            raise
    
    def _get_available_drivers(self, schedule_date: datetime, shift_start: time, shift_end: time) -> List[Driver]:
        """获取可用司机"""
        # 获取所有在职司机
        drivers = self.db.query(Driver).filter(
            Driver.status == 'active',
            Driver.license_expiry > schedule_date.date()
        ).all()
        
        available_drivers = []
        
        for driver in drivers:
            # 检查司机是否已有排班冲突
            if not self._has_schedule_conflict(driver.id, schedule_date, shift_start, shift_end):
                # 检查司机是否满足工作时长限制
                if self._check_work_hours_limit(driver.id, schedule_date, shift_start, shift_end):
                    # 检查司机资质
                    if self._check_driver_qualifications(driver, schedule_date):
                        available_drivers.append(driver)
        
        return available_drivers
    
    def _get_available_vehicles(self, schedule_date: datetime, shift_start: time, shift_end: time) -> List[Vehicle]:
        """获取可用车辆"""
        vehicles = self.db.query(Vehicle).filter(
            Vehicle.status == 'active'
        ).all()
        
        available_vehicles = []
        
        for vehicle in vehicles:
            # 检查车辆是否已有排班冲突
            if not self._has_vehicle_conflict(vehicle.id, schedule_date, shift_start, shift_end):
                # 检查车辆维护状态
                if self._check_vehicle_maintenance(vehicle, schedule_date):
                    available_vehicles.append(vehicle)
        
        return available_vehicles
    
    def _has_schedule_conflict(self, driver_id: int, schedule_date: datetime, start_time: time, end_time: time) -> bool:
        """检查司机排班冲突"""
        existing_schedules = self.db.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.schedule_date == schedule_date.date(),
            Schedule.status.in_(['scheduled', 'in_progress'])
        ).all()
        
        for schedule in existing_schedules:
            if self._time_overlap(start_time, end_time, schedule.start_time, schedule.end_time):
                return True
        
        return False
    
    def _has_vehicle_conflict(self, vehicle_id: int, schedule_date: datetime, start_time: time, end_time: time) -> bool:
        """检查车辆排班冲突"""
        existing_schedules = self.db.query(Schedule).filter(
            Schedule.vehicle_id == vehicle_id,
            Schedule.schedule_date == schedule_date.date(),
            Schedule.status.in_(['scheduled', 'in_progress'])
        ).all()
        
        for schedule in existing_schedules:
            if self._time_overlap(start_time, end_time, schedule.start_time, schedule.end_time):
                return True
        
        return False
    
    def _time_overlap(self, start1: time, end1: time, start2: time, end2: time) -> bool:
        """检查时间重叠"""
        return not (end1 <= start2 or end2 <= start1)
    
    def _check_work_hours_limit(self, driver_id: int, schedule_date: datetime, start_time: time, end_time: time) -> bool:
        """检查工作时长限制"""
        # 获取当天已安排的工时
        existing_schedules = self.db.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.schedule_date == schedule_date.date(),
            Schedule.status.in_(['scheduled', 'in_progress', 'completed'])
        ).all()
        
        total_minutes = 0
        for schedule in existing_schedules:
            start_minutes = schedule.start_time.hour * 60 + schedule.start_time.minute
            end_minutes = schedule.end_time.hour * 60 + schedule.end_time.minute
            total_minutes += end_minutes - start_minutes
        
        # 计算新班次的工时
        new_start_minutes = start_time.hour * 60 + start_time.minute
        new_end_minutes = end_time.hour * 60 + end_time.minute
        new_minutes = new_end_minutes - new_start_minutes
        
        # 检查是否超过最大工作时长（8小时）
        max_daily_hours = 8 * 60  # 8小时转换为分钟
        return (total_minutes + new_minutes) <= max_daily_hours
    
    def _check_driver_qualifications(self, driver: Driver, schedule_date: datetime) -> bool:
        """检查司机资质"""
        # 检查驾照有效期
        if driver.license_expiry <= schedule_date.date():
            return False
        
        # 检查危险品运输证（如果需要）
        # 这里可以添加更多资质检查
        
        return True
    
    def _check_vehicle_maintenance(self, vehicle: Vehicle, schedule_date: datetime) -> bool:
        """检查车辆维护状态"""
        # 检查是否即将需要维护
        if vehicle.maintenance_due_date and vehicle.maintenance_due_date <= schedule_date.date():
            return False
        
        # 检查保险有效期
        if vehicle.insurance_expiry and vehicle.insurance_expiry <= schedule_date.date():
            return False
        
        return True
    
    def _calculate_driver_scores(self, drivers: List[Driver], schedule_date: datetime, preferences: Optional[Dict] = None) -> List[Dict]:
        """计算司机评分"""
        driver_scores = []
        
        for driver in drivers:
            score = 100  # 基础分数
            
            # 经验加分
            if driver.experience_years:
                if driver.experience_years >= 5:
                    score += 10
                elif driver.experience_years >= 3:
                    score += 5
            
            # 安全记录加分
            if driver.safety_rating:
                if driver.safety_rating >= 4.5:
                    score += 15
                elif driver.safety_rating >= 4.0:
                    score += 10
                elif driver.safety_rating >= 3.5:
                    score += 5
            
            # 工作强度调整
            recent_schedules = self._get_recent_driver_schedules(driver.id, 7)  # 最近7天
            if len(recent_schedules) >= 5:  # 最近工作较多
                score -= 10
            elif len(recent_schedules) <= 2:  # 最近工作较少
                score += 5
            
            # 偏好设置
            if preferences:
                if preferences.get('prefer_experienced') and driver.experience_years >= 3:
                    score += 5
                if preferences.get('prefer_high_rating') and driver.safety_rating and driver.safety_rating >= 4.0:
                    score += 5
            
            driver_scores.append({
                'driver': driver,
                'score': max(0, min(150, score))  # 限制分数在0-150之间
            })
        
        # 按分数排序
        driver_scores.sort(key=lambda x: x['score'], reverse=True)
        return driver_scores
    
    def _calculate_vehicle_scores(self, vehicles: List[Vehicle], task_type: str) -> List[Dict]:
        """计算车辆评分"""
        vehicle_scores = []
        
        for vehicle in vehicles:
            score = 100  # 基础分数
            
            # 车辆类型匹配
            if task_type == 'delivery' and vehicle.vehicle_type in ['van', 'truck']:
                score += 10
            elif task_type == 'transport' and vehicle.vehicle_type in ['truck', 'bus']:
                score += 10
            elif task_type == 'pickup' and vehicle.vehicle_type in ['van', 'car']:
                score += 5
            
            # 车辆年龄调整
            if vehicle.purchase_date:
                age_years = (datetime.now().date() - vehicle.purchase_date).days / 365.25
                if age_years <= 2:
                    score += 10
                elif age_years <= 5:
                    score += 5
                elif age_years >= 10:
                    score -= 10
            
            # 里程数调整
            if vehicle.current_mileage:
                if vehicle.current_mileage <= 50000:
                    score += 5
                elif vehicle.current_mileage >= 200000:
                    score -= 10
            
            # 维护状态
            if vehicle.maintenance_due_date:
                days_until_maintenance = (vehicle.maintenance_due_date - datetime.now().date()).days
                if days_until_maintenance <= 7:
                    score -= 20
                elif days_until_maintenance <= 30:
                    score -= 10
            
            vehicle_scores.append({
                'vehicle': vehicle,
                'score': max(0, min(150, score))  # 限制分数在0-150之间
            })
        
        # 按分数排序
        vehicle_scores.sort(key=lambda x: x['score'], reverse=True)
        return vehicle_scores
    
    def _generate_schedules(self, driver_scores: List[Dict], vehicle_scores: List[Dict], 
                           schedule_date: datetime, start_time: time, end_time: time, 
                           task_type: str, required_drivers: int) -> List[Dict]:
        """生成排班方案"""
        schedules = []
        
        # 选择评分最高的司机和车辆组合
        for i in range(min(required_drivers, len(driver_scores))):
            driver_data = driver_scores[i]
            vehicle_data = vehicle_scores[i] if i < len(vehicle_scores) else vehicle_scores[0]
            
            schedule = {
                'driver_id': driver_data['driver'].id,
                'vehicle_id': vehicle_data['vehicle'].id,
                'driver_score': driver_data['score'],
                'vehicle_score': vehicle_data['score'],
                'total_score': driver_data['score'] + vehicle_data['score'],
                'schedule_date': schedule_date,
                'start_time': start_time,
                'end_time': end_time,
                'task_type': task_type,
                'optimization_reason': self._generate_optimization_reason(driver_data, vehicle_data)
            }
            
            schedules.append(schedule)
        
        return schedules
    
    def _generate_optimization_reason(self, driver_data: Dict, vehicle_data: Dict) -> str:
        """生成优化原因说明"""
        reasons = []
        
        driver = driver_data['driver']
        vehicle = vehicle_data['vehicle']
        
        # 司机原因
        if driver.experience_years and driver.experience_years >= 5:
            reasons.append(f"司机{driver.name}经验丰富（{driver.experience_years}年）")
        
        if driver.safety_rating and driver.safety_rating >= 4.5:
            reasons.append(f"司机{driver.name}安全评级优秀（{driver.safety_rating}）")
        
        # 车辆原因
        if vehicle.purchase_date:
            age_years = (datetime.now().date() - vehicle.purchase_date).days / 365.25
            if age_years <= 2:
                reasons.append(f"车辆{vehicle.plate_number}车况较新")
        
        if vehicle.current_mileage and vehicle.current_mileage <= 50000:
            reasons.append(f"车辆{vehicle.plate_number}里程数较低")
        
        return "；".join(reasons) if reasons else "综合评分最优"
    
    def _get_recent_driver_schedules(self, driver_id: int, days: int) -> List[Schedule]:
        """获取司机最近的排班记录"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        return self.db.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.schedule_date >= start_date,
            Schedule.status.in_(['scheduled', 'in_progress', 'completed'])
        ).all()
    
    def check_schedule_conflicts(self, driver_id: int, vehicle_id: int, 
                                schedule_date: datetime, start_time: time, end_time: time) -> Dict:
        """检查排班冲突"""
        conflicts = {
            'has_conflict': False,
            'driver_conflicts': [],
            'vehicle_conflicts': [],
            'work_hours_exceeded': False
        }
        
        # 检查司机冲突
        driver_conflicts = self.db.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.schedule_date == schedule_date.date(),
            Schedule.status.in_(['scheduled', 'in_progress'])
        ).all()
        
        for conflict in driver_conflicts:
            if self._time_overlap(start_time, end_time, conflict.start_time, conflict.end_time):
                conflicts['driver_conflicts'].append({
                    'id': conflict.id,
                    'time': f"{conflict.start_time} - {conflict.end_time}",
                    'status': conflict.status
                })
                conflicts['has_conflict'] = True
        
        # 检查车辆冲突
        vehicle_conflicts = self.db.query(Schedule).filter(
            Schedule.vehicle_id == vehicle_id,
            Schedule.schedule_date == schedule_date.date(),
            Schedule.status.in_(['scheduled', 'in_progress'])
        ).all()
        
        for conflict in vehicle_conflicts:
            if self._time_overlap(start_time, end_time, conflict.start_time, conflict.end_time):
                conflicts['vehicle_conflicts'].append({
                    'id': conflict.id,
                    'time': f"{conflict.start_time} - {conflict.end_time}",
                    'status': conflict.status
                })
                conflicts['has_conflict'] = True
        
        # 检查工作时长
        if not self._check_work_hours_limit(driver_id, schedule_date, start_time, end_time):
            conflicts['work_hours_exceeded'] = True
            conflicts['has_conflict'] = True
        
        return conflicts