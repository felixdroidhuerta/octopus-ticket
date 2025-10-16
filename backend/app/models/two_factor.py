from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class TwoFactorToken(Base):
    __tablename__ = "two_factor_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String(64), nullable=False, unique=True, index=True)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")

    @classmethod
    def expiry(cls, minutes: int = 10) -> datetime:
        return datetime.utcnow() + timedelta(minutes=minutes)
