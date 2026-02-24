from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class EventParticipation(Base):
    __tablename__ = "event_participations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    event = relationship("Event", back_populates="participations")
    person = relationship("Person", back_populates="participations")
    role = relationship("Role", back_populates="participations")
    resource_assignments = relationship("ResourceAssignment", back_populates="participation")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    personnel = relationship("Person", secondary="event_participations", viewonly=True)
    participations = relationship("EventParticipation", back_populates="event")
    location = relationship("Location", back_populates="events")

class ResourceAssignment(Base):
    __tablename__ = "resource_assignments"
    id = Column(Integer, primary_key=True, index=True)
    participation_id = Column(Integer, ForeignKey("event_participations.id"))
    warehouse_stock_id = Column(Integer, ForeignKey("warehouse_stocks.id"))
    assigned_quantity = Column(Integer, nullable=False)
    serial_number = Column(String, nullable=True)
    status = Column(String, default="assigned")
    assignment_date = Column(Date, server_default=func.now())
    delivery_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    participation = relationship("EventParticipation", back_populates="resource_assignments")
    warehouse_stock = relationship("WarehouseStock", back_populates="assignments")

class EventWarehouseStock(Base):
    __tablename__ = "event_warehouse_stocks"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    warehouse_stock_id = Column(Integer, ForeignKey("warehouse_stocks.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    event = relationship("Event", back_populates="warehouse_stocks")
    warehouse_stock = relationship("WarehouseStock", back_populates="events")
