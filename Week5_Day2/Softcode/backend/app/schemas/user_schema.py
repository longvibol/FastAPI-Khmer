from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2)
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


class UserOut(BaseModel):
    id: int
    full_name: str
    gender: Optional[str]
    phone_number: Optional[str]
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
