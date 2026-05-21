from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ProductImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    created_at: datetime


class ProductResponse(BaseModel):
    id: int
    title: str
    original_price: float
    discount_price: Optional[float]
    category_id: int
    colors: List[str] = []
    sizes: List[str] = []
    description: Optional[str]
    main_image: Optional[str]
    is_active: bool
    sub_images: List[str] = []
    created_at: datetime
