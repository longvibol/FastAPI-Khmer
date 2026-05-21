from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.database import Base, engine
from app.config import settings
from app.models import user, category, product, order, payment
from app.routers import auth_router, user_router, category_router, product_router, order_router, payment_router, backup_router, admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = Path(__file__).resolve().parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(payment_router.router)
app.include_router(backup_router.router)
app.include_router(admin_router.router)


@app.get("/")
def root():
    return {"message": "Clothes Ecommerce API is running", "docs": "/docs"}
