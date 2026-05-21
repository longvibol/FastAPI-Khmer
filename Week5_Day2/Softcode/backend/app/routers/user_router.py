from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserOut
from app.core.deps import get_current_admin

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return db.query(User).order_by(User.id.desc()).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
