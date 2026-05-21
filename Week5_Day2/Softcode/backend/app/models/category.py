from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="category")
