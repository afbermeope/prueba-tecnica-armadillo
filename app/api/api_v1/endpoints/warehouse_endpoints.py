from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import warehouse_service as service
from app.schemas import warehouse as schemas
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_warehouses(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Warehouse)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return service.create_warehouse(db=db, warehouse=warehouse)

@router.put("/{warehouse_id}/stock", response_model=schemas.WarehouseStock)
def update_stock(warehouse_id: int, item_id: int, quantity: int, db: Session = Depends(get_db)):
    return service.update_stock(db=db, warehouse_id=warehouse_id, item_id=item_id, quantity=quantity)

@router.get("/{warehouse_id}/stock", response_model=List[schemas.WarehouseStock])
def read_warehouse_stock(warehouse_id: int, db: Session = Depends(get_db)):
    return service.get_warehouse_stock(db=db, warehouse_id=warehouse_id)
