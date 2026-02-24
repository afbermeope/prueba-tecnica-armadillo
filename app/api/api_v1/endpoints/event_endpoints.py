from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import event_service as service
from app.schemas import event as schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return service.create_event(db=db, event=event)

from datetime import date

@router.get("/participations", response_model=List[schemas.EventParticipation])
def read_all_participations(event_id: int = None, person_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_all_participations(db, event_id=event_id, person_id=person_id, skip=skip, limit=limit)

@router.get("/assignments", response_model=List[schemas.AssignmentDetail])
def read_all_assignments(skip: int = 0, limit: int = 100, event_name: str = None, person_name: str = None, item_name: str = None, db: Session = Depends(get_db)):
    return service.get_all_assignments(db, skip=skip, limit=limit, event_name=event_name, person_name=person_name, item_name=item_name)

@router.get("/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, name: str = None, location: str = None, date_from: date = None, date_to: date = None, person_id: int = None, db: Session = Depends(get_db)):
    return service.get_events(db, skip=skip, limit=limit, name=name, location=location, date_from=date_from, date_to=date_to, person_id=person_id)

@router.post("/{event_id}/personnel/{person_id}", response_model=schemas.EventParticipation)
def assign_personnel(event_id: int, person_id: int, role_id: int = None, db: Session = Depends(get_db)):
    return service.assign_personnel(db, event_id=event_id, person_id=person_id, role_id=role_id)
    
@router.post("/{event_id}/resources", response_model=schemas.ResourceAssignment)
def assign_resource(event_id: int, assignment: schemas.ResourceAssignmentCreate, db: Session = Depends(get_db)):
    return service.assign_resources(db, assignment=assignment)

@router.post("/assignments/{assignment_id}/deliver", response_model=schemas.ResourceAssignment)
def deliver_resource(assignment_id: int, db: Session = Depends(get_db)):
    return service.deliver_resource(db, assignment_id=assignment_id)

@router.post("/assignments/{assignment_id}/return", response_model=schemas.ResourceAssignment)
def return_resource(assignment_id: int, db: Session = Depends(get_db)):
    return service.return_resource(db, assignment_id=assignment_id)

@router.delete("/{event_id}/personnel/{person_id}")
def remove_personnel(event_id: int, person_id: int, db: Session = Depends(get_db)):
    return service.remove_personnel(db, event_id=event_id, person_id=person_id)

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    return service.update_event(db=db, event_id=event_id, event=event)

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    service.delete_event(db=db, event_id=event_id)
    return {"detail": "Evento eliminado exitosamente"}
