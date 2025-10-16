from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user, get_db_session
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.from_orm(current_user)


@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_admin),
) -> List[UserOut]:
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [UserOut.from_orm(user) for user in users]


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_admin),
) -> UserOut:
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


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_admin),
) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password" and value:
            user.hashed_password = get_password_hash(value)
        elif field != "password":
            setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut.from_orm(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_admin: User = Depends(get_current_admin),
) -> None:
    if current_admin.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes eliminar tu propio usuario")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
