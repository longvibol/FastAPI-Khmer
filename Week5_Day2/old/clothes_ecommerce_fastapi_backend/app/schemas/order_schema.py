from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: int
    size: Optional[str] = None
    color: Optional[str] = None
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_title: str
    size: Optional[str]
    color: Optional[str]
    quantity: int
    price: float
    subtotal: float


class OrderResponse(BaseModel):
    id: int
    transaction_id: str
    user_id: int
    total_amount: float
    status: str
    payment_method: str
    payment_status: str
    items: List[OrderItemResponse]
    created_at: datetime
