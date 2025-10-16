from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.common import ORMBase


class WikiBase(BaseModel):
    project_id: int
    title: str
    content: str


class WikiCreate(WikiBase):
    author_id: int


class WikiUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]


class WikiOut(WikiBase, ORMBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
