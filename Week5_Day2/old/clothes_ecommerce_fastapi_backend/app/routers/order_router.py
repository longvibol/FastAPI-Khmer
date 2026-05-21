from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order_schema import OrderCreate, OrderStatusUpdate
from app.services.telegram_service import send_telegram_message

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def order_to_dict(order: Order) -> dict:
    return {
        "id": order.id,
        "transaction_id": order.transaction_id,
        "user_id": order.user_id,
        "customer_name": order.user.full_name if order.user else None,
        "customer_phone": order.user.phone_number if order.user else None,
        "total_amount": order.total_amount,
        "status": order.status,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_title": item.product_title,
                "size": item.size,
                "color": item.color,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.subtotal,
            }
            for item in order.items
        ],
    }


@router.post("/")
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    transaction_id = "ORD_" + uuid4().hex[:12].upper()
    order = Order(
        transaction_id=transaction_id,
        user_id=current_user.id,
        total_amount=0,
        status="PENDING",
        payment_method="KHQR",
        payment_status="UNPAID",
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_amount = 0.0
    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        price = product.discount_price if product.discount_price is not None else product.original_price
        subtotal = price * item.quantity
        total_amount += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_title=product.title,
            size=item.size,
            color=item.color,
            quantity=item.quantity,
            price=price,
            subtotal=subtotal,
        )
        db.add(order_item)

    order.total_amount = round(total_amount, 2)
    db.commit()
    db.refresh(order)

    send_telegram_message(
        f"🛒 <b>New Order</b>\n"
        f"Order: <code>{order.transaction_id}</code>\n"
        f"Customer: {current_user.full_name}\n"
        f"Phone: {current_user.phone_number}\n"
        f"Amount: ${order.total_amount:.2f}\n"
        f"Status: {order.payment_status}"
    )

    return order_to_dict(order)


@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.id.desc()).all()
    return [order_to_dict(order) for order in orders]


@router.get("/my-orders")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.id.desc()).all()
    return [order_to_dict(order) for order in orders]


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_to_dict(order)


@router.put("/{order_id}/status")
def update_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = payload.status.upper()
    db.commit()
    db.refresh(order)
    return order_to_dict(order)
