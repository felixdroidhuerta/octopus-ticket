from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Enum as SqlEnum, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    JEFE_PROYECTO = "JEFE_PROYECTO"
    USUARIO = "USUARIO"
    VISUALIZADOR = "VISUALIZADOR"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False, default=UserRole.USUARIO)
    is_active = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    managed_projects = relationship(
        "Project", back_populates="project_manager", cascade="all,delete"
    )
    created_wikis = relationship("WikiPage", back_populates="author")
    reported_tickets = relationship(
        "Ticket", back_populates="reporter", foreign_keys="Ticket.reporter_id"
    )
    assigned_tickets = relationship(
        "Ticket", back_populates="assignee", foreign_keys="Ticket.assignee_id"
    )
    inventory_items = relationship(
        "InventoryItem", back_populates="assigned_user", foreign_keys="InventoryItem.assigned_user_id"
    )
