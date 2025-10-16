from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole
from app.schemas.common import ORMBase


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.USUARIO
    is_active: bool = True
    two_factor_enabled: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    full_name: Optional[str]
    role: Optional[UserRole]
    is_active: Optional[bool]
    password: Optional[str] = Field(default=None, min_length=6)
    two_factor_enabled: Optional[bool]


class UserOut(UserBase, ORMBase):
    id: int
    created_at: datetime
    updated_at: datetime
