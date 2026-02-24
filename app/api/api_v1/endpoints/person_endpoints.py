from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import person_service as service
from app.schemas import person as schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return service.create_person(db=db, person=person)

@router.get("/", response_model=List[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, full_name: str = None, db: Session = Depends(get_db)):
    return service.get_persons(db, skip=skip, limit=limit, full_name=full_name)

@router.get("/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    return service.get_person(db, person_id=person_id)

@router.put("/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return service.update_person(db=db, person_id=person_id, person=person)

@router.delete("/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    service.delete_person(db=db, person_id=person_id)
    return {"detail": "Personal eliminado exitosamente"}
