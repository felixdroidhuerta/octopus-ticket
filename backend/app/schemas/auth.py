from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.user import UserOut


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str] = "bearer"
    user: Optional[UserOut]
    two_factor_required: bool = False
    two_factor_token: Optional[str]
    expires_at: Optional[datetime]
    message: Optional[str]


class TwoFactorVerifyRequest(BaseModel):
    token: str
    code: str
