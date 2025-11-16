from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: str = Field(default="employee", pattern="^(admin|employee)$")
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^(admin|employee)$")
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


class StatisticsResponse(BaseModel):
    total_drivers: int
    active_drivers: int
    new_drivers_this_month: int
    drivers_by_route: List[dict]
    drivers_by_user: List[dict]