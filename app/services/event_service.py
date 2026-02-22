from sqlalchemy.orm import Session
from app.models import event as models
from app.models.person import Person
from app.models.item import Item
from app.models.warehouse import WarehouseStock
from app.schemas import event as schemas
from app.core.exceptions import EntityNotFoundException, IntegrityViolationException
from datetime import date

def create_event(db: Session, event: schemas.EventCreate):
    # Validate: no overlapping events at the same location
    overlapping = db.query(models.Event).filter(
        models.Event.location_id == event.location_id,
        models.Event.start_date <= event.end_date,
        models.Event.end_date >= event.start_date
    ).first()
    
    if overlapping:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un evento en ese lugar entre {overlapping.start_date} y {overlapping.end_date}. "
                   f"Las fechas del nuevo evento ({event.start_date} - {event.end_date}) se solapan."
        )
    
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = get_event(db, event_id)
    if not db_event:
        raise EntityNotFoundException("Event", event_id)
    for var, value in event.dict().items():
        setattr(db_event, var, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = get_event(db, event_id)
    if not db_event:
        raise EntityNotFoundException("Event", event_id)
    db.delete(db_event)
    db.commit()
    return True

def get_events(db: Session, skip: int = 0, limit: int = 100, name: str = None, location: str = None, date_from=None, date_to=None, person_id: int = None):
    query = db.query(models.Event)
    if person_id:
        query = query.filter(models.Event.personnel.any(id=person_id))
    if name:
        query = query.filter(models.Event.name.contains(name))
    if date_from:
        query = query.filter(models.Event.start_date >= date_from)
    if date_to:
        query = query.filter(models.Event.end_date <= date_to)
    return query.offset(skip).limit(limit).all()

def assign_personnel(db: Session, event_id: int, person_id: int, role_id: int = None):
    db_event = get_event(db, event_id)
    if not db_event:
        raise EntityNotFoundException("Event", event_id)
    
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise EntityNotFoundException("Person", person_id)

    db_participation = db.query(models.EventParticipation).filter(
        models.EventParticipation.event_id == event_id,
        models.EventParticipation.person_id == person_id
    ).first()

    if not db_participation:
        db_participation = models.EventParticipation(
            event_id=event_id,
            person_id=person_id,
            role_id=role_id
        )
        db.add(db_participation)
    else:
        if role_id is not None:
            db_participation.role_id = role_id
            
    db.commit()
    db.refresh(db_participation)
    return db_participation

def remove_personnel(db: Session, event_id: int, person_id: int):
    db_participation = db.query(models.EventParticipation).filter(
        models.EventParticipation.event_id == event_id,
        models.EventParticipation.person_id == person_id
    ).first()
    if not db_participation:
        raise EntityNotFoundException("EventParticipation", f"event_id={event_id}, person_id={person_id}")
    db.delete(db_participation)
    db.commit()
    return True

def assign_resources(db: Session, assignment: schemas.ResourceAssignmentCreate):
    # Check participation
    db_participation = db.query(models.EventParticipation).filter(
        models.EventParticipation.id == assignment.participation_id
    ).first()
    if not db_participation:
        raise EntityNotFoundException("EventParticipation", assignment.participation_id)
    
    # Check stock
    db_stock = db.query(WarehouseStock).filter(
        WarehouseStock.id == assignment.warehouse_stock_id
    ).first()
    if not db_stock:
        raise EntityNotFoundException("WarehouseStock", assignment.warehouse_stock_id)
        
    if db_stock.quantity < assignment.assigned_quantity:
        raise IntegrityViolationException(f"Insufficient stock. Available: {db_stock.quantity}")

    db_assignment = models.ResourceAssignment(**assignment.dict())
    
    # Deduct quantity
    db_stock.quantity -= assignment.assigned_quantity
    
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def deliver_resource(db: Session, assignment_id: int):
    db_assignment = db.query(models.ResourceAssignment).filter(models.ResourceAssignment.id == assignment_id).first()
    if not db_assignment:
        raise EntityNotFoundException("ResourceAssignment", assignment_id)
    
    db_assignment.status = "delivered"
    db_assignment.delivery_date = date.today()
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def return_resource(db: Session, assignment_id: int):
    db_assignment = db.query(models.ResourceAssignment).filter(models.ResourceAssignment.id == assignment_id).first()
    if not db_assignment:
        raise EntityNotFoundException("ResourceAssignment", assignment_id)
    
    db_stock = db.query(WarehouseStock).filter(
        WarehouseStock.id == db_assignment.warehouse_stock_id
    ).first()
    
    if db_stock:
        db_stock.quantity += db_assignment.assigned_quantity
    
    db_assignment.status = "returned"
    db_assignment.return_date = date.today()
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_all_assignments(db: Session, skip: int = 0, limit: int = 100, event_name: str = None, person_name: str = None, item_name: str = None):
    from app.models.warehouse import Warehouse, WarehouseStock
    from app.models.item import Item
    
    query = db.query(
        models.ResourceAssignment.id.label("assignment_id"),
        models.Event.name.label("event_name"),
        models.Event.start_date.label("event_start_date"),
        models.Event.end_date.label("event_end_date"),
        Person.full_name.label("person_name"),
        Item.name.label("item_name"),
        models.ResourceAssignment.assigned_quantity.label("assigned_quantity"),
        Warehouse.name.label("warehouse_name"),
        models.ResourceAssignment.status.label("status"),
        models.ResourceAssignment.assignment_date.label("assignment_date"),
        models.ResourceAssignment.delivery_date.label("delivery_date"),
        models.ResourceAssignment.return_date.label("return_date"),
    ).select_from(models.ResourceAssignment) \
     .join(models.EventParticipation, models.ResourceAssignment.participation_id == models.EventParticipation.id) \
     .join(models.Event, models.EventParticipation.event_id == models.Event.id) \
     .join(Person, models.EventParticipation.person_id == Person.id) \
     .join(WarehouseStock, models.ResourceAssignment.warehouse_stock_id == WarehouseStock.id) \
     .join(Item, WarehouseStock.item_id == Item.id) \
     .join(Warehouse, WarehouseStock.warehouse_id == Warehouse.id)
    if event_name:
        query = query.filter(models.Event.name.ilike(f"%{event_name}%"))
    if person_name:
        query = query.filter(Person.full_name.ilike(f"%{person_name}%"))
    if item_name:
        query = query.filter(Item.name.ilike(f"%{item_name}%"))
    return query.offset(skip).limit(limit).all()

def get_all_participations(db: Session, event_id: int = None, person_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.EventParticipation)
    if event_id:
        query = query.filter(models.EventParticipation.event_id == event_id)
    if person_id:
        query = query.filter(models.EventParticipation.person_id == person_id)
    return query.offset(skip).limit(limit).all()
