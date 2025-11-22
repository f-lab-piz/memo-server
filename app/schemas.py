from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MemoBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str


class MemoCreate(MemoBase):
    pass


class MemoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None


class MemoRead(MemoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
