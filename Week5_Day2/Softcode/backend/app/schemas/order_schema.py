from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    size: Optional[str] = None
    color: Optional[str] = None
    quantity: int = 1


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_title: str
    size: Optional[str]
    color: Optional[str]
    quantity: int
    price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    transaction_id: str
    user_id: int
    total_amount: float
    status: str
    payment_method: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
