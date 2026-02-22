from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    capacity = Column(Integer, nullable=True)
    
    # Relationships
    events = relationship("Event", back_populates="location")
