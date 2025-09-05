from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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
