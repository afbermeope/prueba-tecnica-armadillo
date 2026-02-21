from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.resource import ResourceItem
from app.schemas.event import Event

# Warehouse Departure
class WarehouseDepartureBase(BaseModel):
    responsible_person: str

class WarehouseDepartureCreate(WarehouseDepartureBase):
    item_ids: List[int]

class WarehouseDeparture(WarehouseDepartureBase):
    id: int
    departure_date: datetime
    class Config:
        from_attributes = True

# Departure Item
class DepartureItemBase(BaseModel):
    departure_id: int
    item_id: int
    return_date: Optional[datetime] = None

class DepartureItem(DepartureItemBase):
    id: int
    class Config:
        from_attributes = True

class DepartureDetail(WarehouseDeparture):
    items: List[ResourceItem]
    events: List[Event]
