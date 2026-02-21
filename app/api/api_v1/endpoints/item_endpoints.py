from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import resource_service as service
from app.schemas import resource as schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ResourceItem)
def create_item(item: schemas.ResourceItemCreate, db: Session = Depends(get_db)):
    return service.create_item(db=db, item=item)

@router.get("/", response_model=List[schemas.ResourceItem])
def read_items(skip: int = 0, limit: int = 100, status: str = None, serial_number: str = None, category_id: int = None, db: Session = Depends(get_db)):
    return service.get_items(db, skip=skip, limit=limit, status=status, serial_number=serial_number, category_id=category_id)

@router.get("/{item_id}/history", response_model=List[schemas.ItemHistory])
def read_item_history(item_id: int, db: Session = Depends(get_db)):
    return service.get_item_history(db, item_id=item_id)
