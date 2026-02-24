from sqlalchemy.orm import Session
from app.models import warehouse as models
from app.schemas import warehouse as schemas
from app.core.exceptions import EntityNotFoundException

def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def update_stock(db: Session, warehouse_id: int, item_id: int, quantity: int):
    from sqlalchemy.exc import IntegrityError
    from fastapi import HTTPException
    from app.models.item import Item
    
    # Validar que exista el warehouse
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise EntityNotFoundException("Warehouse", warehouse_id)
    
    # Validar que exista el item
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise EntityNotFoundException("Item", item_id)
    
    # Validar que exista el stock
    db_stock = db.query(models.WarehouseStock).filter(
        models.WarehouseStock.warehouse_id == warehouse_id,
        models.WarehouseStock.item_id == item_id
    ).first()
    
    if db_stock:
        db_stock.quantity = quantity
    else:
        db_stock = models.WarehouseStock(
            warehouse_id=warehouse_id,
            item_id=item_id,
            quantity=quantity
        )
        db.add(db_stock)
    
    try:
        db.commit()
        db.refresh(db_stock)
        return db_stock
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Error de integridad al actualizar el stock")

def get_warehouse_stock(db: Session, warehouse_id: int):
    return db.query(models.WarehouseStock).filter(models.WarehouseStock.warehouse_id == warehouse_id).all()

def get_all_stocks(db: Session, warehouse_id: int = None, item_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.WarehouseStock)
    if warehouse_id:
        query = query.filter(models.WarehouseStock.warehouse_id == warehouse_id)
    if item_id:
        query = query.filter(models.WarehouseStock.item_id == item_id)
    return query.offset(skip).limit(limit).all()
