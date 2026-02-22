from pydantic import BaseModel, EmailStr
from typing import Optional

class PersonBase(BaseModel):
    full_name: str
    identification_number: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    class Config:
        from_attributes = True
