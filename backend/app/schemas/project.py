from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.common import ORMBase


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_manager_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    project_manager_id: Optional[int]


class ProjectOut(ProjectBase, ORMBase):
    id: int
    created_at: datetime
    updated_at: datetime
