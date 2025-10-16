import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models  # noqa: F401
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.user import User, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_startup_admin() -> None:
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.first_superuser_email).first()
        if not admin:
            admin = User(
                email=settings.first_superuser_email,
                full_name="Administrador",
                role=UserRole.ADMIN,
                hashed_password=get_password_hash(settings.first_superuser_password),
                two_factor_enabled=False,
            )
            db.add(admin)
            db.commit()
            logger.info("Usuario administrador inicial creado: %s", admin.email)
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    create_startup_admin()


app = FastAPI(title=settings.app_name)


if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
