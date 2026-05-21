import json
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.payment import Payment
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.payment_schema import CheckoutResponse, VerifyResponse
from app.services.khqr_service import create_checkout_url, verify_transaction, is_payment_success
from app.services.telegram_service import send_telegram_alert

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.get("/checkout/{order_id}", response_model=CheckoutResponse)
def checkout(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    checkout_url = create_checkout_url(
        transaction_id=order.transaction_id,
        amount=order.total_amount,
        remark=f"Web Order #{order.id}",
    )
    order.payment_status = "PENDING"
    db.commit()

    return CheckoutResponse(order_id=order.id, transaction_id=order.transaction_id, checkout_url=checkout_url)


@router.post("/verify/{transaction_id}", response_model=VerifyResponse)
def verify_payment(transaction_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.transaction_id == transaction_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    result = verify_transaction(transaction_id)
    paid = is_payment_success(result)

    if paid:
        order.payment_status = "PAID"
        order.status = "PAID"
        data = result.get("data", {})
        payment = db.query(Payment).filter(Payment.transaction_id == transaction_id).first()
        if not payment:
            payment = Payment(
                order_id=order.id,
                transaction_id=transaction_id,
                amount=float(data.get("amount", order.total_amount)),
                status="SUCCESS",
                gateway_response=json.dumps(result),
                payment_date=data.get("payment_date"),
            )
            db.add(payment)
        else:
            payment.status = "SUCCESS"
            payment.gateway_response = json.dumps(result)
        db.commit()

        send_telegram_alert(
            f"✅ <b>Payment Success</b>\nOrder: {transaction_id}\nAmount: ${order.total_amount:.2f}"
        )
        return VerifyResponse(transaction_id=transaction_id, is_paid=True, status="success")

    order.payment_status = "FAILED" if result.get("responseCode") != 1 else "PENDING"
    db.commit()
    return VerifyResponse(transaction_id=transaction_id, is_paid=False, status=str(result.get("responseMessage", "pending")))


@router.get("/success")
def payment_success(request: Request, db: Session = Depends(get_db)):
    transaction_id = request.query_params.get("transaction_id") or request.query_params.get("tran_id")
    if not transaction_id:
        # Gateway may return different params. Frontend can still call verify manually.
        return {"message": "Payment callback received. Please verify transaction from frontend.", "params": dict(request.query_params)}

    # Verify immediately after redirect
    verify_payment(transaction_id, db)
    return RedirectResponse(url=f"http://localhost:3000/payment-success?transaction_id={transaction_id}")
