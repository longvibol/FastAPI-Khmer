from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product, ProductImage
from app.models.category import Category
from app.models.user import User
from app.schemas.product_schema import ProductOut
from app.core.deps import get_current_admin
from app.services.file_service import save_upload_file

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("/", response_model=ProductOut)
def create_product(
    title: str = Form(...),
    original_price: float = Form(...),
    discount_price: Optional[float] = Form(None),
    category_id: Optional[int] = Form(None),
    colors: Optional[str] = Form(None),
    sizes: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    main_image: Optional[UploadFile] = File(None),
    sub_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    if category_id:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    main_image_path = None
    if main_image:
        try:
            main_image_path = save_upload_file(main_image, "main")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    product = Product(
        title=title,
        original_price=original_price,
        discount_price=discount_price,
        category_id=category_id,
        colors=colors,
        sizes=sizes,
        description=description,
        main_image=main_image_path,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    if sub_images:
        for img in sub_images:
            if img and img.filename:
                try:
                    path = save_upload_file(img, "sub")
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))
                db.add(ProductImage(product_id=product.id, image_url=path))
        db.commit()
        db.refresh(product)

    return product


@router.get("/", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).order_by(Product.id.desc()).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/category/{category_id}", response_model=list[ProductOut])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.category_id == category_id, Product.is_active == True).all()


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
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
    admin: User = Depends(get_current_admin),
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
        product.category_id = category_id
    if colors is not None:
        product.colors = colors
    if sizes is not None:
        product.sizes = sizes
    if description is not None:
        product.description = description
    if main_image:
        product.main_image = save_upload_file(main_image, "main")

    if sub_images:
        for img in sub_images:
            if img and img.filename:
                db.add(ProductImage(product_id=product.id, image_url=save_upload_file(img, "sub")))

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_active = False
    db.commit()
    return {"message": "Product disabled"}
