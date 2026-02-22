from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import location_service as service
from app.schemas import location as schemas
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_locations(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return service.create_location(db=db, location=location)

@router.get("/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    return service.get_location(db=db, location_id=location_id)
