from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import TokenResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Password and confirm password do not match")

    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_phone = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    user = User(
        full_name=payload.full_name,
        gender=payload.gender,
        phone_number=payload.phone_number,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }
