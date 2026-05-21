from pydantic import BaseModel


class CheckoutResponse(BaseModel):
    order_id: int
    transaction_id: str
    checkout_url: str


class VerifyResponse(BaseModel):
    transaction_id: str
    is_paid: bool
    status: str
