from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: str = Field(default="employee", pattern="^(superadmin|admin|dispatcher|manager|driver|auditor|employee)$")
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^(superadmin|admin|dispatcher|manager|driver|auditor|employee)$")
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DriverBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    id_card: str = Field(..., pattern=r"^\d{17}[\dXx]$")
    license_number: str = Field(..., min_length=5, max_length=20)
    license_type: str = Field(..., min_length=1, max_length=20)
    main_route: str = Field(..., min_length=2, max_length=200)
    vehicle_type: str = Field(..., min_length=2, max_length=50)
    vehicle_length: Optional[str] = Field(None, max_length=20)
    price_per_km: Decimal = Field(default=0.00, ge=0)
    experience_years: int = Field(default=0, ge=0)
    status: str = Field(default="active", pattern="^(active|inactive|blocked)$")
    region_type: str = Field(default="国内", pattern="^(国内|国外)$")
    emergency_contact: Optional[str] = Field(None, max_length=50)
    emergency_phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$")
    remark: Optional[str] = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$")
    id_card: Optional[str] = Field(None, pattern=r"^\d{17}[\dXx]$")
    license_number: Optional[str] = Field(None, min_length=5, max_length=20)
    license_type: Optional[str] = Field(None, min_length=1, max_length=20)
    main_route: Optional[str] = Field(None, min_length=2, max_length=200)
    vehicle_type: Optional[str] = Field(None, min_length=2, max_length=50)
    vehicle_length: Optional[str] = Field(None, max_length=20)
    price_per_km: Optional[Decimal] = Field(None, ge=0)
    experience_years: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|inactive|blocked)$")
    region_type: Optional[str] = Field(None, pattern="^(国内|国外)$")
    emergency_contact: Optional[str] = Field(None, max_length=50)
    emergency_phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$")
    remark: Optional[str] = None


class DriverResponse(DriverBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


class DriverListResponse(BaseModel):
    data: List[DriverResponse]
    total: int
    page: int
    page_size: int


class DriverPhotoBase(BaseModel):
    photo_type: str = Field(..., pattern="^(id_card_front|id_card_back|license|vehicle)$")
    file_name: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None


class DriverPhotoResponse(DriverPhotoBase):
    id: int
    driver_id: int
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class VehicleBase(BaseModel):
    plate_number: str = Field(..., min_length=5, max_length=20)
    vehicle_type: str = Field(..., min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    color: Optional[str] = Field(None, max_length=20)
    engine_number: Optional[str] = Field(None, max_length=50)
    vin_number: Optional[str] = Field(None, max_length=50)
    purchase_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    insurance_expiry: Optional[datetime] = None
    annual_inspection_date: Optional[datetime] = None
    maintenance_due_date: Optional[datetime] = None
    mileage: Decimal = Field(default=0.00, ge=0)
    fuel_type: Optional[str] = Field(None, max_length=20)
    fuel_consumption: Decimal = Field(default=0.00, ge=0)
    status: str = Field(default="active", pattern="^(active|maintenance|retired)$")
    current_driver_id: Optional[int] = None


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = Field(None, min_length=5, max_length=20)
    vehicle_type: Optional[str] = Field(None, min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    color: Optional[str] = Field(None, max_length=20)
    engine_number: Optional[str] = Field(None, max_length=50)
    vin_number: Optional[str] = Field(None, max_length=50)
    purchase_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    insurance_expiry: Optional[datetime] = None
    annual_inspection_date: Optional[datetime] = None
    maintenance_due_date: Optional[datetime] = None
    mileage: Optional[Decimal] = Field(None, ge=0)
    fuel_type: Optional[str] = Field(None, max_length=20)
    fuel_consumption: Optional[Decimal] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|maintenance|retired)$")
    current_driver_id: Optional[int] = None


class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    current_driver_id: Optional[int] = None

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    driver_id: int
    vehicle_id: Optional[int] = None
    schedule_date: datetime
    start_time: datetime
    end_time: datetime
    route: Optional[str] = Field(None, max_length=200)
    task_type: str = Field(..., pattern="^(delivery|pickup|transport)$")
    status: str = Field(default="scheduled", pattern="^(scheduled|in_progress|completed|cancelled)$")
    notes: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    schedule_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    route: Optional[str] = Field(None, max_length=200)
    task_type: Optional[str] = Field(None, pattern="^(delivery|pickup|transport)$")
    status: Optional[str] = Field(None, pattern="^(scheduled|in_progress|completed|cancelled)$")
    notes: Optional[str] = None


class ScheduleResponse(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    driver: Optional[DriverResponse] = None
    vehicle: Optional[VehicleResponse] = None
    
    class Config:
        from_attributes = True


class DriverCertificateBase(BaseModel):
    driver_id: int
    certificate_type: str = Field(..., min_length=2, max_length=50)
    certificate_number: str = Field(..., min_length=5, max_length=100)
    issue_date: Optional[datetime] = None
    expiry_date: datetime
    issuing_authority: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="valid", pattern="^(valid|expired|suspended)$")
    file_path: Optional[str] = None


class DriverCertificateCreate(DriverCertificateBase):
    pass


class DriverCertificateUpdate(BaseModel):
    certificate_type: Optional[str] = Field(None, min_length=2, max_length=50)
    certificate_number: Optional[str] = Field(None, min_length=5, max_length=100)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    issuing_authority: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, pattern="^(valid|expired|suspended)$")
    file_path: Optional[str] = None


class DriverCertificateResponse(DriverCertificateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    driver: Optional[DriverResponse] = None
    
    class Config:
        from_attributes = True


class MaintenanceRecordBase(BaseModel):
    vehicle_id: int
    maintenance_type: str = Field(..., pattern="^(routine|repair|inspection)$")
    description: Optional[str] = None
    cost: Decimal = Field(default=0.00, ge=0)
    mileage_at_service: Optional[Decimal] = Field(None, ge=0)
    service_date: datetime
    next_service_date: Optional[datetime] = None
    service_provider: Optional[str] = Field(None, max_length=100)
    invoice_number: Optional[str] = Field(None, max_length=50)
    status: str = Field(default="completed", pattern="^(scheduled|in_progress|completed)$")


class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass


class MaintenanceRecordUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    maintenance_type: Optional[str] = Field(None, pattern="^(routine|repair|inspection)$")
    description: Optional[str] = None
    cost: Optional[Decimal] = Field(None, ge=0)
    mileage_at_service: Optional[Decimal] = Field(None, ge=0)
    service_date: Optional[datetime] = None
    next_service_date: Optional[datetime] = None
    service_provider: Optional[str] = Field(None, max_length=100)
    invoice_number: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, pattern="^(scheduled|in_progress|completed)$")


class MaintenanceRecordResponse(MaintenanceRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    vehicle: Optional[VehicleResponse] = None
    
    class Config:
        from_attributes = True


class GPSRecordBase(BaseModel):
    vehicle_id: int
    driver_id: Optional[int] = None
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)
    speed: Decimal = Field(default=0.00, ge=0)
    heading: Optional[Decimal] = Field(None, ge=0, le=360)
    altitude: Optional[Decimal] = None
    accuracy: Optional[Decimal] = Field(None, ge=0)
    timestamp: datetime
    address: Optional[str] = Field(None, max_length=200)
    status: Optional[str] = Field(None, pattern="^(normal|speeding|idle)$")


class GPSRecordCreate(GPSRecordBase):
    pass


class GPSRecordResponse(GPSRecordBase):
    id: int
    created_at: datetime
    vehicle: Optional[VehicleResponse] = None
    driver: Optional[DriverResponse] = None
    
    class Config:
        from_attributes = True


class DrivingBehaviorBase(BaseModel):
    driver_id: int
    vehicle_id: Optional[int] = None
    behavior_type: str = Field(..., pattern="^(harsh_braking|speeding|sharp_turn)$")
    severity: str = Field(..., pattern="^(low|medium|high)$")
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    speed_at_event: Optional[Decimal] = Field(None, ge=0)
    timestamp: datetime
    description: Optional[str] = None
    processed: bool = False


class DrivingBehaviorCreate(DrivingBehaviorBase):
    pass


class DrivingBehaviorUpdate(BaseModel):
    processed: bool


class DrivingBehaviorResponse(DrivingBehaviorBase):
    id: int
    created_at: datetime
    driver: Optional[DriverResponse] = None
    vehicle: Optional[VehicleResponse] = None
    
    class Config:
        from_attributes = True


class EmergencyAlertBase(BaseModel):
    driver_id: int
    vehicle_id: Optional[int] = None
    alert_type: str = Field(..., pattern="^(accident|medical|security)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    description: Optional[str] = None
    status: str = Field(default="active", pattern="^(active|responded|resolved)$")
    responded_by: Optional[int] = None
    response_time: Optional[datetime] = None


class EmergencyAlertCreate(EmergencyAlertBase):
    pass


class EmergencyAlertUpdate(BaseModel):
    status: str = Field(..., pattern="^(active|responded|resolved)$")
    responded_by: Optional[int] = None
    response_time: Optional[datetime] = None


class EmergencyAlertResponse(EmergencyAlertBase):
    id: int
    created_at: datetime
    updated_at: datetime
    driver: Optional[DriverResponse] = None
    vehicle: Optional[VehicleResponse] = None
    responder: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


class StatisticsResponse(BaseModel):
    total_drivers: int
    active_drivers: int
    new_drivers_this_month: int
    drivers_by_route: List[dict]
    drivers_by_user: List[dict]
    total_vehicles: int
    active_vehicles: int
    total_schedules: int
    completed_schedules: int
    expired_certificates: int
    upcoming_maintenance: int
    active_emergency_alerts: int


class ReminderResponse(BaseModel):
    type: str = Field(..., pattern="^(certificate_expiry|insurance_expiry|inspection_expiry)$")
    days_before: int = Field(..., ge=1, le=365)
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    vehicle_plate: Optional[str] = None
    certificate_type: Optional[str] = None
    certificate_number: Optional[str] = None
    expiry_date: datetime
    user_email: Optional[str] = None
    user_role: Optional[str] = None


class ReminderSettings(BaseModel):
    reminder_days: Optional[List[int]] = Field(None, description="提前提醒天数列表")
    enabled: Optional[bool] = Field(True, description="是否启用提醒")
    notification_methods: Optional[List[str]] = Field(None, description="通知方式: email, sms, push")
    default_days_ahead: Optional[int] = Field(30, ge=1, le=365, description="默认提前天数")