from typing import Optional
from pydantic import BaseModel

class ContactBase(BaseModel):
    name: str
    email: str
    phone: str
    address: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class ConfigDict:
        from_attributes = True