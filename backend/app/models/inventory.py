from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class InventoryType(str, Enum):
    TELEFONO = "TELEFONO"
    ORDENADOR = "ORDENADOR"
    TABLET = "TABLET"
    MONITOR = "MONITOR"
    OTRO = "OTRO"


class InventoryStatus(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    ASIGNADO = "ASIGNADO"
    MANTENIMIENTO = "MANTENIMIENTO"


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(SqlEnum(InventoryType), nullable=False)
    serial_number = Column(String(255), unique=True, nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    status = Column(SqlEnum(InventoryStatus), nullable=False, default=InventoryStatus.DISPONIBLE)
    purchase_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    assigned_user = relationship("User", back_populates="inventory_items")
    project = relationship("Project", back_populates="inventory_items")
