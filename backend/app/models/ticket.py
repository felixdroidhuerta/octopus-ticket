from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class TicketPriority(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"


class TicketStatus(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROGRESO = "EN_PROGRESO"
    EN_REVISION = "EN_REVISION"
    COMPLETADO = "COMPLETADO"
    CERRADO = "CERRADO"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(SqlEnum(TicketPriority), nullable=False, default=TicketPriority.MEDIA)
    status = Column(SqlEnum(TicketStatus), nullable=False, default=TicketStatus.PENDIENTE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    project = relationship("Project", back_populates="tickets")
    reporter = relationship("User", back_populates="reported_tickets", foreign_keys=[reporter_id])
    assignee = relationship("User", back_populates="assigned_tickets", foreign_keys=[assignee_id])
