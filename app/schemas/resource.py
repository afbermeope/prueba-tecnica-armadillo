from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# Resource Category
class ResourceCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ResourceCategoryCreate(ResourceCategoryBase):
    pass

class ResourceCategory(ResourceCategoryBase):
    id: int
    class Config:
        from_attributes = True

# Resource Item
class ResourceItemBase(BaseModel):
    category_id: int
    serial_number: str
    status: str = "in_warehouse"

class ResourceItemCreate(ResourceItemBase):
    pass

class ResourceItem(ResourceItemBase):
    id: int
    class Config:
        from_attributes = True

# Traceability Schemas
class ItemHistory(BaseModel):
    event_name: str
    event_date: date
    departure_date: datetime
    return_date: Optional[datetime]
    location: str
