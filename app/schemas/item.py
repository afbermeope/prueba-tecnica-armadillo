from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ItemBase(BaseModel):
    name: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: Optional[str] = None

class Item(ItemBase):
    id: int
    
    class Config:
        from_attributes = True

class ItemHistory(BaseModel):
    event_name: str
    start_date: date
    end_date: date
    assignment_date: date
    delivery_date: Optional[date]
    return_date: Optional[date]
    location: str
    warehouse_name: str
    status: str
    
    class Config:
        from_attributes = True
