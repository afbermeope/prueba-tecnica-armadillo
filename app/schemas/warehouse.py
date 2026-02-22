from pydantic import BaseModel
from typing import List, Optional

from app.schemas import item as item_schemas

class WarehouseStockBase(BaseModel):
    warehouse_id: int
    item_id: int
    quantity: int

class WarehouseStock(WarehouseStockBase):
    id: int
    item: item_schemas.Item
    
    class Config:
        from_attributes = True

class WarehouseBase(BaseModel):
    name: str
    location: Optional[str] = None
    address: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int
    stocks: List[WarehouseStock] = []
    class Config:
        from_attributes = True
