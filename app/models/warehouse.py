from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=True) # City or zone
    address = Column(String, nullable=True)
    
    # Relationships
    stocks = relationship("WarehouseStock", back_populates="warehouse")

class WarehouseStock(Base):
    __tablename__ = "warehouse_stocks"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=0)
    
    warehouse = relationship("Warehouse", back_populates="stocks")
    item = relationship("Item", back_populates="warehouse_stocks")
    assignments = relationship("ResourceAssignment", back_populates="warehouse_stock")
