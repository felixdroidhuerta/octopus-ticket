from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.ticket import TicketPriority, TicketStatus
from app.schemas.common import ORMBase


class TicketBase(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.MEDIA
    status: TicketStatus = TicketStatus.PENDIENTE
    assignee_id: Optional[int] = None


class TicketCreate(TicketBase):
    reporter_id: int


class TicketUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[TicketPriority]
    status: Optional[TicketStatus]
    assignee_id: Optional[int]


class TicketOut(TicketBase, ORMBase):
    id: int
    reporter_id: int
    created_at: datetime
    updated_at: datetime
