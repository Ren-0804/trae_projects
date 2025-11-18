from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="employee")
    is_active = Column(Boolean, default=True, index=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    drivers = relationship("Driver", back_populates="user", cascade="all, delete-orphan")
    operation_logs = relationship("OperationLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    id_card = Column(String(18), unique=True, nullable=False, index=True)
    license_number = Column(String(20), unique=True, nullable=False, index=True)
    license_type = Column(String(20), nullable=False, index=True)
    main_route = Column(String(200), nullable=False, index=True)
    vehicle_type = Column(String(50), nullable=False)
    vehicle_length = Column(String(20), nullable=True)
    price_per_km = Column(DECIMAL(10, 2), default=0.00)
    experience_years = Column(Integer, default=0)
    status = Column(String(20), nullable=False, default="active", index=True)
    region_type = Column(String(10), nullable=False, default="国内", index=True)
    emergency_contact = Column(String(50), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="drivers")
    photos = relationship("DriverPhoto", back_populates="driver", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Driver(id={self.id}, name={self.name}, phone={self.phone})>"


class DriverPhoto(Base):
    __tablename__ = "driver_photos"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    photo_type = Column(String(50), nullable=False, index=True)  # id_card_front, id_card_back, license, vehicle
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(200), nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # 关联关系
    driver = relationship("Driver", back_populates="photos")
    
    def __repr__(self):
        return f"<DriverPhoto(id={self.id}, driver_id={self.driver_id}, type={self.photo_type})>"


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, nullable=False, index=True)
    vehicle_type = Column(String(50), nullable=False, index=True)
    brand = Column(String(50), nullable=True)
    model = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)
    color = Column(String(20), nullable=True)
    engine_number = Column(String(50), nullable=True)
    vin_number = Column(String(50), unique=True, nullable=True, index=True)
    purchase_date = Column(DateTime, nullable=True)
    registration_date = Column(DateTime, nullable=True)
    insurance_expiry = Column(DateTime, nullable=True)
    annual_inspection_date = Column(DateTime, nullable=True)
    maintenance_due_date = Column(DateTime, nullable=True)
    mileage = Column(DECIMAL(10, 2), default=0.00)
    fuel_type = Column(String(20), nullable=True)
    fuel_consumption = Column(DECIMAL(5, 2), default=0.00)
    status = Column(String(20), nullable=False, default="active", index=True)  # active, maintenance, retired
    current_driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    current_driver = relationship("Driver", foreign_keys=[current_driver_id])
    assignments = relationship("VehicleAssignment", back_populates="vehicle", cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="vehicle", cascade="all, delete-orphan")
    gps_records = relationship("GPSRecord", back_populates="vehicle", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Vehicle(id={self.id}, plate_number={self.plate_number})>"


class VehicleAssignment(Base):
    __tablename__ = "vehicle_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    assignment_type = Column(String(20), nullable=False, index=True)  # primary, temporary
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=True, index=True)
    status = Column(String(20), nullable=False, default="active", index=True)  # active, completed, cancelled
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    vehicle = relationship("Vehicle", back_populates="assignments")
    driver = relationship("Driver")
    
    def __repr__(self):
        return f"<VehicleAssignment(id={self.id}, vehicle_id={self.vehicle_id}, driver_id={self.driver_id})>"


class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True, index=True)
    schedule_date = Column(DateTime, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    route = Column(String(200), nullable=True)
    task_type = Column(String(50), nullable=False, index=True)  # delivery, pickup, transport
    status = Column(String(20), nullable=False, default="scheduled", index=True)  # scheduled, in_progress, completed, cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    driver = relationship("Driver")
    vehicle = relationship("Vehicle")
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, driver_id={self.driver_id}, date={self.schedule_date})>"


class DriverCertificate(Base):
    __tablename__ = "driver_certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    certificate_type = Column(String(50), nullable=False, index=True)  # license, dangerous_goods, etc.
    certificate_number = Column(String(100), nullable=False, index=True)
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=False, index=True)
    issuing_authority = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="valid", index=True)  # valid, expired, suspended
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    driver = relationship("Driver")
    
    def __repr__(self):
        return f"<DriverCertificate(id={self.id}, driver_id={self.driver_id}, type={self.certificate_type})>"


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    maintenance_type = Column(String(50), nullable=False, index=True)  # routine, repair, inspection
    description = Column(Text, nullable=True)
    cost = Column(DECIMAL(10, 2), default=0.00)
    mileage_at_service = Column(DECIMAL(10, 2), nullable=True)
    service_date = Column(DateTime, nullable=False, index=True)
    next_service_date = Column(DateTime, nullable=True, index=True)
    service_provider = Column(String(100), nullable=True)
    invoice_number = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="completed", index=True)  # scheduled, in_progress, completed
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    vehicle = relationship("Vehicle", back_populates="maintenance_records")
    
    def __repr__(self):
        return f"<MaintenanceRecord(id={self.id}, vehicle_id={self.vehicle_id}, type={self.maintenance_type})>"


class GPSRecord(Base):
    __tablename__ = "gps_records"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True, index=True)
    latitude = Column(DECIMAL(10, 7), nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7), nullable=False, index=True)
    speed = Column(DECIMAL(5, 2), default=0.00)
    heading = Column(DECIMAL(5, 2), nullable=True)
    altitude = Column(DECIMAL(8, 2), nullable=True)
    accuracy = Column(DECIMAL(5, 2), nullable=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    address = Column(String(200), nullable=True)
    status = Column(String(20), nullable=True, index=True)  # normal, speeding, idle
    created_at = Column(DateTime, default=func.now())
    
    # 关联关系
    vehicle = relationship("Vehicle", back_populates="gps_records")
    driver = relationship("Driver")
    
    def __repr__(self):
        return f"<GPSRecord(id={self.id}, vehicle_id={self.vehicle_id}, lat={self.latitude}, lng={self.longitude})>"


class DrivingBehavior(Base):
    __tablename__ = "driving_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True, index=True)
    behavior_type = Column(String(50), nullable=False, index=True)  # harsh_braking, speeding, sharp_turn
    severity = Column(String(20), nullable=False, index=True)  # low, medium, high
    latitude = Column(DECIMAL(10, 7), nullable=True)
    longitude = Column(DECIMAL(10, 7), nullable=True)
    speed_at_event = Column(DECIMAL(5, 2), nullable=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    description = Column(Text, nullable=True)
    processed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # 关联关系
    driver = relationship("Driver")
    vehicle = relationship("Vehicle")
    
    def __repr__(self):
        return f"<DrivingBehavior(id={self.id}, driver_id={self.driver_id}, type={self.behavior_type})>"


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True, index=True)
    alert_type = Column(String(50), nullable=False, index=True)  # accident, medical, security
    severity = Column(String(20), nullable=False, index=True)  # low, medium, high, critical
    latitude = Column(DECIMAL(10, 7), nullable=True)
    longitude = Column(DECIMAL(10, 7), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="active", index=True)  # active, responded, resolved
    responded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    response_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    driver = relationship("Driver")
    vehicle = relationship("Vehicle")
    responder = relationship("User", foreign_keys=[responded_by])
    
    def __repr__(self):
        return f"<EmergencyAlert(id={self.id}, driver_id={self.driver_id}, type={self.alert_type})>"


class OperationLog(Base):
    __tablename__ = "operation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    operation_type = Column(String(50), nullable=False, index=True)
    table_name = Column(String(50), nullable=False, index=True)
    record_id = Column(Integer, nullable=False, index=True)
    old_data = Column(Text, nullable=True)  # JSON字符串
    new_data = Column(Text, nullable=True)  # JSON字符串
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    
    # 关联关系
    user = relationship("User", back_populates="operation_logs")
    
    def __repr__(self):
        return f"<OperationLog(id={self.id}, user_id={self.user_id}, operation={self.operation_type})>"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    due_date = Column(DateTime, nullable=True, index=True)
    priority = Column(String(20), nullable=False, default="medium", index=True)  # low, medium, high, critical
    status = Column(String(20), nullable=False, default="draft", index=True)  # draft, assigned, accepted, onroad, arrived, completed, abnormal
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    assignee = relationship("User")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"


class TaskEvent(Base):
    __tablename__ = "task_events"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # assign, update_status, note, abnormal
    content = Column(Text, nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=func.now(), index=True)

    task = relationship("Task")
    actor = relationship("User")


class FileAsset(Base):
    __tablename__ = "file_assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=True)
    size = Column(Integer, nullable=True)
    path = Column(String(500), nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    related_type = Column(String(50), nullable=True, index=True)
    related_id = Column(String(50), nullable=True, index=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now(), index=True)

    uploader = relationship("User")


# 创建索引
Index("idx_drivers_user_created", Driver.user_id, Driver.created_at.desc())
Index("idx_operation_logs_user_created", OperationLog.user_id, OperationLog.created_at.desc())
Index("idx_vehicles_plate_number", Vehicle.plate_number)
Index("idx_vehicles_status", Vehicle.status)
Index("idx_schedules_date", Schedule.schedule_date)
Index("idx_schedules_driver_date", Schedule.driver_id, Schedule.schedule_date)
Index("idx_certificates_driver_expiry", DriverCertificate.driver_id, DriverCertificate.expiry_date)
Index("idx_gps_records_vehicle_timestamp", GPSRecord.vehicle_id, GPSRecord.timestamp.desc())
Index("idx_driving_behaviors_driver_timestamp", DrivingBehavior.driver_id, DrivingBehavior.timestamp.desc())
Index("idx_emergency_alerts_status", EmergencyAlert.status)
Index("idx_tasks_status", Task.status)
Index("idx_task_events_task_created", TaskEvent.task_id, TaskEvent.created_at.desc())
Index("idx_file_assets_related", FileAsset.related_type, FileAsset.related_id)