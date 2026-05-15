from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str = "Apple"
    price: float = 10.5
    stock: int = 10

@app.post("/items/")
def create_items(
        item: Product,
        discount: float = 0,
        buy_Qty: int = 0
):
    final_price = (item.price -discount) * item.stock
    Remain_Stock = item.stock - buy_Qty

    return {
        "item_name": item.name,
        "original_price": item.price,
        "discount_applied": discount,
        "final_price": final_price,
        "stock": Remain_Stock
    }