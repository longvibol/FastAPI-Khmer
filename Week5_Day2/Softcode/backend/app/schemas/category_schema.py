from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
