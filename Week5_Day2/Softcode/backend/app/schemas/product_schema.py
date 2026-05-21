from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductImageOut(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    title: str
    original_price: float
    discount_price: Optional[float]
    category_id: Optional[int]
    colors: Optional[str]
    sizes: Optional[str]
    description: Optional[str]
    main_image: Optional[str]
    is_active: bool
    created_at: datetime
    images: List[ProductImageOut] = []

    class Config:
        from_attributes = True
