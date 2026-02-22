from pydantic import BaseModel, field_validator
from datetime import date
from typing import List, Optional
from app.schemas.person import Person
from app.schemas.role import Role

# Event
class EventBase(BaseModel):
    name: str
    location_id: int
    start_date: date
    end_date: date

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def set_default_date(cls, v):
        return v if v is not None else date.today()

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    personnel: List[Person] = []
    class Config:
        from_attributes = True

# Event Assignment (Warehouse Link) - Deprecated or keep for traceability?
# User asked for ResourceAssignment linking Person + Item + Event
class EventAssignmentCreate(BaseModel):
    departure_item_id: int
    event_id: int

# Event Participation
class EventParticipationBase(BaseModel):
    event_id: int
    person_id: int
    role_id: Optional[int] = None

class EventParticipationCreate(EventParticipationBase):
    pass

class EventParticipation(EventParticipationBase):
    id: int
    role: Optional[Role] = None
    class Config:
        from_attributes = True

# New Resource Assignment (Person + Item + Event)
class ResourceAssignmentBase(BaseModel):
    participation_id: int
    warehouse_stock_id: int
    assigned_quantity: int
    serial_number: Optional[str] = None
    status: str = "assigned"
    delivery_date: Optional[date] = None
    return_date: Optional[date] = None

class ResourceAssignmentCreate(ResourceAssignmentBase):
    pass

class ResourceAssignment(ResourceAssignmentBase):
    id: int
    assignment_date: date
    class Config:
        from_attributes = True
