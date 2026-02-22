from sqlalchemy.orm import Session
from app.models.person import Person
from app.schemas.person import PersonCreate
from app.core.exceptions import EntityNotFoundException, IntegrityViolationException

def create_person(db: Session, person: PersonCreate):
    existing = db.query(Person).filter(Person.identification_number == person.identification_number).first()
    if existing:
        raise IntegrityViolationException(f"Person with identification {person.identification_number} already exists")
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_person(db: Session, person_id: int):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise EntityNotFoundException("Person", person_id)
    return db_person

def get_persons(db: Session, skip: int = 0, limit: int = 100, full_name: str = None):
    query = db.query(Person)
    if full_name:
        query = query.filter(Person.full_name.contains(full_name))
    return query.offset(skip).limit(limit).all()

def update_person(db: Session, person_id: int, person: PersonCreate):
    db_person = get_person(db, person_id)
    
    # Check if new identification already exists
    if person.identification_number != db_person.identification_number:
        existing = db.query(Person).filter(Person.identification_number == person.identification_number).first()
        if existing:
            raise IntegrityViolationException(f"Person with identification {person.identification_number} already exists")
            
    for var, value in person.dict().items():
        setattr(db_person, var, value)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id)
    db.delete(db_person)
    db.commit()
    return True
