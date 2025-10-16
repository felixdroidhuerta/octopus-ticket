import logging
import secrets
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.two_factor import TwoFactorToken
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    Token,
    TwoFactorVerifyRequest,
)
from app.schemas.user import UserCreate, UserOut

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db_session),
) -> LoginResponse:
    email = login_data.email
    password = login_data.password

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

    if user.two_factor_enabled:
        token_value = uuid4().hex
        code = f"{secrets.randbelow(1000000):06d}"
        expires_at = TwoFactorToken.expiry()

        db.query(TwoFactorToken).filter(TwoFactorToken.user_id == user.id).delete(synchronize_session=False)
        two_factor = TwoFactorToken(
            user_id=user.id,
            token=token_value,
            code=code,
            expires_at=expires_at,
        )
        db.add(two_factor)
        db.commit()
        logger.info("2FA CODE for %s: %s", user.email, code)

        return LoginResponse(
            two_factor_required=True,
            two_factor_token=token_value,
            expires_at=expires_at,
            message="Se ha enviado un código de verificación",
        )

    access_token = create_access_token(user.email)
    return LoginResponse(access_token=access_token, user=UserOut.from_orm(user))


@router.post("/verify-2fa", response_model=Token)
def verify_two_factor(request: TwoFactorVerifyRequest, db: Session = Depends(get_db_session)) -> Token:
    record = (
        db.query(TwoFactorToken)
        .filter(TwoFactorToken.token == request.token)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token 2FA no encontrado")

    if record.expires_at < datetime.utcnow():
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código expirado")

    if record.code != request.code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código inválido")

    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

    access_token = create_access_token(user.email)
    db.delete(record)
    db.commit()

    return Token(access_token=access_token, user=UserOut.from_orm(user))


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db_session)) -> UserOut:
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=user_in.is_active,
        two_factor_enabled=user_in.two_factor_enabled,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut.from_orm(user)
