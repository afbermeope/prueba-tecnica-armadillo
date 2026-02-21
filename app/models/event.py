from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    date = Column(Date)
    
    assignments = relationship("EventAssignment", back_populates="event")

class EventAssignment(Base):
    __tablename__ = "event_assignments"
    id = Column(Integer, primary_key=True, index=True)
    departure_item_id = Column(Integer, ForeignKey("departure_items.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    
    departure_item = relationship("DepartureItem", back_populates="assignments")
    event = relationship("Event", back_populates="assignments")
