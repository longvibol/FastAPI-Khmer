from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.models import *  # noqa: F401,F403 - Import models before create_all
from app.routers import (
    auth_router,
    backup_router,
    category_router,
    order_router,
    payment_router,
    product_router,
    user_router,
)

Path("app/uploads/products/main").mkdir(parents=True, exist_ok=True)
Path("app/uploads/products/sub").mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(payment_router.router)
app.include_router(backup_router.router)


@app.get("/")
def root():
    return {
        "message": "Clothes Ecommerce FastAPI Backend is running",
        "docs": "/docs",
    }
