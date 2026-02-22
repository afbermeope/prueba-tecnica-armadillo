from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    identification_number = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Relationships
    participations = relationship("EventParticipation", back_populates="person")
    # Many-to-many with Event will be defined via association table in event.py or here
