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

@router.get("/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, name: str = None, location: str = None, date_from: date = None, date_to: date = None, db: Session = Depends(get_db)):
    return service.get_events(db, skip=skip, limit=limit, name=name, location=location, date_from=date_from, date_to=date_to)
