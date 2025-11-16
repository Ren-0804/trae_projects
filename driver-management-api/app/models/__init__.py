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


# 创建索引
Index("idx_drivers_user_created", Driver.user_id, Driver.created_at.desc())
Index("idx_operation_logs_user_created", OperationLog.user_id, OperationLog.created_at.desc())