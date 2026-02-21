from pydantic import BaseModel
from datetime import date

# Event
class EventBase(BaseModel):
    name: str
    location: str
    date: date

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    class Config:
        from_attributes = True

# Event Assignment
class EventAssignmentCreate(BaseModel):
    departure_item_id: int
    event_id: int
