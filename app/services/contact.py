from pytest import Session
from sqlalchemy.exc import IntegrityError

from app.models.contact import Contact
from app.schemas.contact import ContactCreate


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    if contact.email:
        is_email_exists = db.query(Contact).filter(Contact.email == contact.email).first()
        if is_email_exists:
            raise IntegrityError("Email already exists", None, None)

    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    if contact.email:
        is_email_exists = db.query(Contact).filter(Contact.email == contact.email, Contact.id != contact_id).first()
        if is_email_exists:
            raise IntegrityError("Email already exists", None, None)
    
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None
