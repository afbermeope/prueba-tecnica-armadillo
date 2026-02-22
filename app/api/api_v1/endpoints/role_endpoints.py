from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import role_service as service
from app.schemas import role as schemas
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_roles(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return service.create_role(db=db, role=role)

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: Session = Depends(get_db)):
    return service.get_role(db=db, role_id=role_id)
