from pydantic import BaseModel
from typing import Optional, List

class LocationBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    capacity: Optional[int] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    
    class Config:
        from_attributes = True
