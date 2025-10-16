from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.models.inventory import InventoryStatus, InventoryType
from app.schemas.common import ORMBase


class InventoryBase(BaseModel):
    name: str
    type: InventoryType
    serial_number: str
    assigned_user_id: Optional[int] = None
    assigned_project_id: Optional[int] = None
    status: InventoryStatus = InventoryStatus.DISPONIBLE
    purchase_date: Optional[date] = None
    notes: Optional[str] = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    name: Optional[str]
    type: Optional[InventoryType]
    serial_number: Optional[str]
    assigned_user_id: Optional[int]
    assigned_project_id: Optional[int]
    status: Optional[InventoryStatus]
    purchase_date: Optional[date]
    notes: Optional[str]


class InventoryOut(InventoryBase, ORMBase):
    id: int
    created_at: datetime
    updated_at: datetime
