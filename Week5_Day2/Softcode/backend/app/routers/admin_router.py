from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.category import Category
from app.core.deps import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
def stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    total_sales = sum([o.total_amount for o in db.query(Order).filter(Order.payment_status == "PAID").all()])
    return {
        "users": db.query(User).count(),
        "products": db.query(Product).count(),
        "categories": db.query(Category).count(),
        "orders": db.query(Order).count(),
        "paid_orders": db.query(Order).filter(Order.payment_status == "PAID").count(),
        "total_sales": round(total_sales, 2),
    }
