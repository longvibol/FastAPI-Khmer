import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order_schema import OrderCreate, OrderOut, OrderStatusUpdate
from app.core.deps import get_current_user, get_current_admin
from app.services.telegram_service import send_telegram_alert

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut)
def create_order(data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not data.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    transaction_id = f"ORD_{int(time.time())}_{current_user.id}"
    order = Order(transaction_id=transaction_id, user_id=current_user.id, total_amount=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    total = 0
    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")
        price = product.discount_price if product.discount_price else product.original_price
        subtotal = price * item.quantity
        total += subtotal
        db.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_title=product.title,
            size=item.size,
            color=item.color,
            quantity=item.quantity,
            price=price,
            subtotal=subtotal,
        ))

    order.total_amount = round(total, 2)
    db.commit()
    db.refresh(order)

    send_telegram_alert(
        f"🛒 <b>New Order</b>\nOrder: {order.transaction_id}\nCustomer: {current_user.full_name}\nAmount: ${order.total_amount:.2f}"
    )
    return order


@router.get("/", response_model=list[OrderOut])
def get_all_orders(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return db.query(Order).order_by(Order.id.desc()).all()


@router.get("/my-orders", response_model=list[OrderOut])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.id.desc()).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return order


@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = data.status
    db.commit()
    db.refresh(order)
    return order
