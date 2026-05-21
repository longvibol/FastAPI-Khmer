import json
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.product import Product, ProductImage
from app.services.file_service import save_upload_file

router = APIRouter(prefix="/api/products", tags=["Products"])


def parse_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    try:
        data = json.loads(value)
        if isinstance(data, list):
            return [str(item).strip() for item in data if str(item).strip()]
    except Exception:
        pass
    return [item.strip() for item in value.split(",") if item.strip()]


def product_to_dict(product: Product) -> dict:
    return {
        "id": product.id,
        "title": product.title,
        "original_price": product.original_price,
        "discount_price": product.discount_price,
        "category_id": product.category_id,
        "category_name": product.category.name if product.category else None,
        "colors": parse_list(product.colors),
        "sizes": parse_list(product.sizes),
        "description": product.description,
        "main_image": product.main_image,
        "sub_images": [img.image_url for img in product.images],
        "is_active": product.is_active,
        "created_at": product.created_at,
    }


@router.post("/")
async def create_product(
    title: str = Form(...),
    original_price: float = Form(...),
    discount_price: Optional[float] = Form(None),
    category_id: int = Form(...),
    colors: Optional[str] = Form(None),
    sizes: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    main_image: UploadFile = File(...),
    sub_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    main_image_url = await save_upload_file(main_image, "app/uploads/products/main")

    product = Product(
        title=title,
        original_price=original_price,
        discount_price=discount_price,
        category_id=category_id,
        colors=json.dumps(parse_list(colors)),
        sizes=json.dumps(parse_list(sizes)),
        description=description,
        main_image=main_image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    if sub_images:
        for image in sub_images:
            if image and image.filename:
                image_url = await save_upload_file(image, "app/uploads/products/sub")
                db.add(ProductImage(product_id=product.id, image_url=image_url))
        db.commit()
        db.refresh(product)

    return product_to_dict(product)


@router.get("/")
def get_products(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.is_active == True)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))

    products = query.order_by(Product.id.desc()).offset(skip).limit(limit).all()
    return [product_to_dict(product) for product in products]


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_dict(product)


@router.get("/category/{category_id}")
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .filter(Product.category_id == category_id, Product.is_active == True)
        .order_by(Product.id.desc())
        .all()
    )
    return [product_to_dict(product) for product in products]


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    title: Optional[str] = Form(None),
    original_price: Optional[float] = Form(None),
    discount_price: Optional[float] = Form(None),
    category_id: Optional[int] = Form(None),
    colors: Optional[str] = Form(None),
    sizes: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    main_image: Optional[UploadFile] = File(None),
    sub_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if title is not None:
        product.title = title
    if original_price is not None:
        product.original_price = original_price
    if discount_price is not None:
        product.discount_price = discount_price
    if category_id is not None:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = category_id
    if colors is not None:
        product.colors = json.dumps(parse_list(colors))
    if sizes is not None:
        product.sizes = json.dumps(parse_list(sizes))
    if description is not None:
        product.description = description
    if main_image and main_image.filename:
        product.main_image = await save_upload_file(main_image, "app/uploads/products/main")

    if sub_images:
        for image in sub_images:
            if image and image.filename:
                image_url = await save_upload_file(image, "app/uploads/products/sub")
                db.add(ProductImage(product_id=product.id, image_url=image_url))

    db.commit()
    db.refresh(product)
    return product_to_dict(product)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_active = False
    db.commit()
    return {"message": "Product deactivated successfully"}
