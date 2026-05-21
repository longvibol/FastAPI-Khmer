from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.core.deps import get_current_user
from app.database import get_db
from app.models.order import Order
from app.models.payment import Payment
from app.models.user import User
from app.services.khqr_service import build_checkout_url, verify_transaction
from app.services.telegram_service import send_telegram_message

router = APIRouter(prefix="/api/payments", tags=["Payments"])


def save_payment_result(db: Session, order: Order, result: dict):
    payment = db.query(Payment).filter(Payment.transaction_id == order.transaction_id).first()
    if not payment:
        payment = Payment(
            order_id=order.id,
            transaction_id=order.transaction_id,
            amount=order.total_amount,
        )
        db.add(payment)

    payment.status = "PAID" if result.get("is_paid") else "FAILED"
    payment.gateway_response = result.get("raw_json")

    if result.get("is_paid"):
        payment.payment_date = datetime.utcnow()
        order.payment_status = "PAID"
        order.status = "PAID"
    else:
        order.payment_status = "PENDING"

    db.commit()
    db.refresh(payment)
    db.refresh(order)
    return payment


@router.get("/checkout/{order_id}")
def create_checkout_session(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You cannot pay this order")

    success_url = f"{settings.SITE_SUCCESS_URL}?transaction_id={order.transaction_id}"
    remark = f"Web Order {order.transaction_id}"

    checkout_url = build_checkout_url(
        transaction_id=order.transaction_id,
        amount=order.total_amount,
        success_url=success_url,
        remark=remark,
    )

    return {
        "order_id": order.id,
        "transaction_id": order.transaction_id,
        "amount": order.total_amount,
        "checkout_url": checkout_url,
    }


@router.get("/success")
def payment_success_callback(
    transaction_id: str = Query(...),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.transaction_id == transaction_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    result = verify_transaction(transaction_id)
    save_payment_result(db, order, result)

    if result.get("is_paid"):
        send_telegram_message(
            f"✅ <b>Payment Success</b>\n"
            f"Order: <code>{order.transaction_id}</code>\n"
            f"Amount: ${order.total_amount:.2f}\n"
            f"Customer: {order.user.full_name if order.user else 'N/A'}"
        )
        return {
            "message": "Payment verified successfully",
            "transaction_id": transaction_id,
            "status": "PAID",
        }

    return {
        "message": "Payment not verified yet",
        "transaction_id": transaction_id,
        "status": result.get("status", "PENDING"),
        "gateway_message": result.get("message"),
    }


@router.post("/verify/{transaction_id}")
def verify_payment_manually(transaction_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.transaction_id == transaction_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    result = verify_transaction(transaction_id)
    save_payment_result(db, order, result)

    if result.get("is_paid"):
        send_telegram_message(
            f"✅ <b>Payment Verified</b>\n"
            f"Order: <code>{order.transaction_id}</code>\n"
            f"Amount: ${order.total_amount:.2f}"
        )

    return {
        "transaction_id": transaction_id,
        "is_paid": result.get("is_paid"),
        "status": "PAID" if result.get("is_paid") else result.get("status", "PENDING"),
        "amount": result.get("amount"),
        "message": result.get("message"),
    }
