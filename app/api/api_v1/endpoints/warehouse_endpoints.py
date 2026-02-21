from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services import departure_service as service
from app.schemas import departure as schemas
from app.schemas import resource as resource_schemas
from app.db.session import get_db

from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[schemas.WarehouseDeparture])
def read_departures(skip: int = 0, limit: int = 100, responsible_person: str = None, date_from: datetime = None, date_to: datetime = None, db: Session = Depends(get_db)):
    return service.get_departures(db, skip=skip, limit=limit, responsible_person=responsible_person, date_from=date_from, date_to=date_to)

@router.post("/", response_model=schemas.WarehouseDeparture)
def create_departure(departure: schemas.WarehouseDepartureCreate, db: Session = Depends(get_db)):
    return service.create_departure(db=db, departure=departure)

@router.get("/{departure_id}/items", response_model=List[resource_schemas.ResourceItem])
def read_departure_items(departure_id: int, db: Session = Depends(get_db)):
    return service.get_items_by_departure(db, departure_id=departure_id)

@router.post("/assign", status_code=201)
def assign_to_events(departure_item_ids: List[int], event_ids: List[int], db: Session = Depends(get_db)):
    return service.assign_items_to_events(db, departure_item_ids=departure_item_ids, event_ids=event_ids)

@router.post("/return", status_code=200)
def return_resources(departure_item_ids: List[int], db: Session = Depends(get_db)):
    service.return_items(db, departure_item_ids=departure_item_ids)
    return {"message": "Items returned successfully"}
