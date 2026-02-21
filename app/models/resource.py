from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class ResourceCategory(Base):
    __tablename__ = "resource_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    items = relationship("ResourceItem", back_populates="category")

class ResourceItem(Base):
    __tablename__ = "resource_items"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("resource_categories.id"))
    serial_number = Column(String, unique=True, index=True)
    status = Column(String, default="in_warehouse") # in_warehouse, out, maintenance
    
    category = relationship("ResourceCategory", back_populates="items")
    departure_items = relationship("DepartureItem", back_populates="item")
