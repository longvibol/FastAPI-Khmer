from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from app.core.deps import get_current_admin

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    exists = db.query(Category).filter(Category.name == data.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(name=data.name, parent_id=data.parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id.desc()).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if data.name is not None:
        category.name = data.name
    if data.parent_id is not None:
        category.parent_id = data.parent_id
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
