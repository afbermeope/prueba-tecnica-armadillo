from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class WarehouseDeparture(Base):
    __tablename__ = "warehouse_departures"
    id = Column(Integer, primary_key=True, index=True)
    departure_date = Column(DateTime, server_default=func.now())
    responsible_person = Column(String)
    
    items = relationship("DepartureItem", back_populates="departure")

class DepartureItem(Base):
    __tablename__ = "departure_items"
    id = Column(Integer, primary_key=True, index=True)
    departure_id = Column(Integer, ForeignKey("warehouse_departures.id"))
    item_id = Column(Integer, ForeignKey("resource_items.id"))
    return_date = Column(DateTime, nullable=True)
    
    departure = relationship("WarehouseDeparture", back_populates="items")
    item = relationship("ResourceItem", back_populates="departure_items")
    assignments = relationship("EventAssignment", back_populates="departure_item")
