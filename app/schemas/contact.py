from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name must be between 1 and 100 characters")
    email: EmailStr = Field(..., description="Must be a valid email address")
    phone: str = Field(..., pattern=r'^\+\d{9,15}$', description="Phone number must be between 9 and 15 digits, and can start with +")
    address: Optional[str] = Field(None, max_length=255, description="Address can be up to 255 characters")

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty or just whitespace')
        return v.strip()

    @field_validator('phone')
    def phone_must_be_valid(cls, v):
        if not v.startswith('+'):
            if not v.isdigit() or len(v) != 10:
                raise ValueError('Phone number must be 10 digits if not starting with +')
        return v

class ContactCreate(ContactBase):
    name: str = Field(..., min_length=1, max_length=100, description="Name must be between 1 and 100 characters")
    email: EmailStr = Field(..., description="Must be a valid email address")
    phone: str = Field(..., pattern=r'^\+\d{9,15}$', description="Phone number must be between 9 and 15 digits, and can start with +")
    address: Optional[str] = Field(None, max_length=255, description="Address can be up to 255 characters")

class ContactUpdate(ContactBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name must be between 1 and 100 characters")
    email: Optional[EmailStr] = Field(None, description="Must be a valid email address")
    phone: Optional[str] = Field(None, pattern=r'^\+\d{9,15}$', description="Phone number must be between 9 and 15 digits, and can start with +")
    address: Optional[str] = Field(None, max_length=255, description="Address can be up to 255 characters")

class Contact(ContactBase):
    id: int

    class ConfigDict:
        from_attributes = True