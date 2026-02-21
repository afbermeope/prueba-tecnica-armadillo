from sqlalchemy.orm import Session
from app.models import departure as models
from app.models.resource import ResourceItem
from app.models.event import EventAssignment
from app.schemas import departure as schemas
from datetime import datetime

def create_departure(db: Session, departure: schemas.WarehouseDepartureCreate):
    db_departure = models.WarehouseDeparture(responsible_person=departure.responsible_person)
    db.add(db_departure)
    db.flush()
    
    for item_id in departure.item_ids:
        item = db.query(ResourceItem).filter(ResourceItem.id == item_id).first()
        if item:
            item.status = "out"
            dep_item = models.DepartureItem(departure_id=db_departure.id, item_id=item_id)
            db.add(dep_item)
    
    db.commit()
    db.refresh(db_departure)
    return db_departure

def get_items_by_departure(db: Session, departure_id: int):
    return db.query(ResourceItem).join(models.DepartureItem).filter(models.DepartureItem.departure_id == departure_id).all()

def get_departures(db: Session, skip: int = 0, limit: int = 100, responsible_person: str = None, date_from = None, date_to = None):
    query = db.query(models.WarehouseDeparture)
    if responsible_person:
        query = query.filter(models.WarehouseDeparture.responsible_person.contains(responsible_person))
    if date_from:
        query = query.filter(models.WarehouseDeparture.departure_date >= date_from)
    if date_to:
        query = query.filter(models.WarehouseDeparture.departure_date <= date_to)
    return query.offset(skip).limit(limit).all()

def assign_items_to_events(db: Session, departure_item_ids: list[int], event_ids: list[int]):
    assignments = []
    for di_id in departure_item_ids:
        for ev_id in event_ids:
            assignment = EventAssignment(departure_item_id=di_id, event_id=ev_id)
            db.add(assignment)
            assignments.append(assignment)
    db.commit()
    return assignments

def return_items(db: Session, departure_item_ids: list[int]):
    for di_id in departure_item_ids:
        dep_item = db.query(models.DepartureItem).filter(models.DepartureItem.id == di_id).first()
        if dep_item:
            dep_item.return_date = datetime.now()
            item = db.query(ResourceItem).filter(ResourceItem.id == dep_item.item_id).first()
            if item:
                item.status = "in_warehouse"
    db.commit()
