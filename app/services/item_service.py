from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Ya existe un ítem con el nombre '{item.name}'")

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_item_history(db: Session, item_id: int):
    from app.models.event import Event, ResourceAssignment, EventParticipation
    from app.models.warehouse import Warehouse, WarehouseStock
    from app.models.location import Location
    
    results = db.query(
        Event.name.label("event_name"),
        Event.start_date.label("start_date"),
        Event.end_date.label("end_date"),
        ResourceAssignment.assignment_date.label("assignment_date"),
        ResourceAssignment.delivery_date.label("delivery_date"),
        ResourceAssignment.return_date.label("return_date"),
        Location.name.label("location"),
        Warehouse.name.label("warehouse_name"),
        ResourceAssignment.status.label("status")
    ).select_from(ResourceAssignment) \
     .join(EventParticipation, ResourceAssignment.participation_id == EventParticipation.id) \
     .join(Event, EventParticipation.event_id == Event.id) \
     .join(Location, Event.location_id == Location.id) \
     .join(WarehouseStock, ResourceAssignment.warehouse_stock_id == WarehouseStock.id) \
     .join(Warehouse, WarehouseStock.warehouse_id == Warehouse.id) \
     .filter(WarehouseStock.item_id == item_id).all()
    return results
