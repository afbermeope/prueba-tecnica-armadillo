from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services import resource_service as service
from app.schemas import resource as schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ResourceCategory)
def create_category(category: schemas.ResourceCategoryCreate, db: Session = Depends(get_db)):
    return service.create_category(db=db, category=category)

@router.get("/", response_model=List[schemas.ResourceCategory])
def read_categories(skip: int = 0, limit: int = 100, name: str = None, db: Session = Depends(get_db)):
    return service.get_categories(db, skip=skip, limit=limit, name=name)
