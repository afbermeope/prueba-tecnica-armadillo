from sqlalchemy.orm import Session
from app.models import resource as models
from app.schemas import resource as schemas

def create_category(db: Session, category: schemas.ResourceCategoryCreate):
    db_category = models.ResourceCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100, name: str = None):
    query = db.query(models.ResourceCategory)
    if name:
        query = query.filter(models.ResourceCategory.name.contains(name))
    return query.offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100, status: str = None, serial_number: str = None, category_id: int = None):
    query = db.query(models.ResourceItem)
    if status:
        query = query.filter(models.ResourceItem.status == status)
    if serial_number:
        query = query.filter(models.ResourceItem.serial_number.contains(serial_number))
    if category_id:
        query = query.filter(models.ResourceItem.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ResourceItemCreate):
    db_item = models.ResourceItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_history(db: Session, item_id: int):
    from app.models.event import Event, EventAssignment
    from app.models.departure import WarehouseDeparture, DepartureItem
    
    results = db.query(
        Event.name.label("event_name"),
        Event.date.label("event_date"),
        WarehouseDeparture.departure_date.label("departure_date"),
        DepartureItem.return_date.label("return_date"),
        Event.location.label("location")
    ).join(EventAssignment, Event.id == EventAssignment.event_id) \
     .join(DepartureItem, EventAssignment.departure_item_id == DepartureItem.id) \
     .join(WarehouseDeparture, DepartureItem.departure_id == WarehouseDeparture.id) \
     .filter(DepartureItem.item_id == item_id).all()
    return results
