from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import item_service as service
from app.schemas import item as schemas
from app.db.session import get_db
from app.models.item import Item

router = APIRouter()

@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_items(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return service.create_item(db=db, item=item)

@router.get("/{item_id}/history", response_model=List[schemas.ItemHistory])
def read_item_history(item_id: int, db: Session = Depends(get_db)):
    return service.get_item_history(db, item_id=item_id)

@router.put("/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return service.update_item(db=db, item_id=item_id, item=item)

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    service.delete_item(db=db, item_id=item_id)
    return {"detail": "Item eliminado exitosamente"}
