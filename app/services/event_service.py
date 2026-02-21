from sqlalchemy.orm import Session
from app.models import event as models
from app.schemas import event as schemas

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100, name: str = None, location: str = None, date_from = None, date_to = None):
    query = db.query(models.Event)
    if name:
        query = query.filter(models.Event.name.contains(name))
    if location:
        query = query.filter(models.Event.location.contains(location))
    if date_from:
        query = query.filter(models.Event.date >= date_from)
    if date_to:
        query = query.filter(models.Event.date <= date_to)
    return query.offset(skip).limit(limit).all()
