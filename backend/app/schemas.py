from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ---------- Auth ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "public"
    shelter_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Users ----------
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    shelter_id: Optional[int] = None

    class Config:
        from_attributes = True  # pydantic v2: serialize from ORM


# ---------- Shelter ----------
class ShelterBase(BaseModel):
    name: str
    address: str
    geo_lat: float = Field(ge=-90, le=90)
    geo_lng: float = Field(ge=-180, le=180)
    phone: Optional[str] = None
    policies: Optional[str] = None
    hours: Optional[str] = None

class ShelterCreate(ShelterBase):
    pass

class ShelterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    geo_lat: Optional[float] = None
    geo_lng: Optional[float] = None
    phone: Optional[str] = None
    policies: Optional[str] = None
    hours: Optional[str] = None

class ShelterOut(ShelterBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ---------- Capacity ----------
class CapacityUpdate(BaseModel):
    beds_total: int = Field(ge=0)
    beds_available: int = Field(ge=0)

class CapacityLogOut(BaseModel):
    id: int
    shelter_id: int
    beds_total: int
    beds_available: int
    updated_at: datetime
    updated_by: Optional[int] = None
    class Config:
        from_attributes = True

# ---------- Intake ----------
class IntakeRequestCreate(BaseModel):
    shelter_id: int
    name: Optional[str] = None
    reason: Optional[str] = None
    eta: Optional[datetime] = None  # expected arrival

class IntakeRequestOut(BaseModel):
    id: int
    shelter_id: int
    name: Optional[str]
    reason: Optional[str]
    eta: Optional[datetime]
    created_at: datetime
    class Config:
        from_attributes = True