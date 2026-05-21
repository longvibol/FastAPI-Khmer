from typing import Optional

from pydantic import BaseModel


class CheckoutResponse(BaseModel):
    order_id: int
    transaction_id: str
    amount: float
    checkout_url: str


class VerifyPaymentResponse(BaseModel):
    transaction_id: str
    is_paid: bool
    status: str
    amount: Optional[float] = None
    message: str
