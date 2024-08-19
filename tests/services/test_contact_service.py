import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.contact import Base
from app.schemas.contact import ContactCreate
from app.services.contact import get_contact, get_contacts, create_contact, update_contact, delete_contact

# Setup the database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_contact(db):
    """
    Test the creation of a new contact.

    Steps:
    1. Create a ContactCreate object with name, email, and phone.
    2. Call the create_contact service with the ContactCreate object.
    3. Assert that the returned contact has the correct name, email, and phone.
    """
    contact_data = ContactCreate(name="John Doe", email="john.doe@example.com", phone="+123456789")
    contact = create_contact(db, contact_data)
    assert contact.name == "John Doe"
    assert contact.email == "john.doe@example.com"
    assert contact.phone == "+123456789"

def test_get_contact(db):
    """
    Test retrieving a specific contact by ID.

    Steps:
    1. Create a ContactCreate object with name, email, and phone.
    2. Call the create_contact service to create the contact.
    3. Call the get_contact service with the created contact's ID.
    4. Assert that the fetched contact has the correct ID, name, email, and phone.
    """
    contact_data = ContactCreate(name="Jane Doe", email="jane.doe@example.com", phone="+987654321")
    created_contact = create_contact(db, contact_data)
    fetched_contact = get_contact(db, created_contact.id)
    assert fetched_contact.id == created_contact.id
    assert fetched_contact.name == "Jane Doe"
    assert fetched_contact.email == "jane.doe@example.com"
    assert fetched_contact.phone == "+987654321"

def test_get_contacts(db):
    """
    Test retrieving the list of contacts.

    Steps:
    1. Create two ContactCreate objects with different names, emails, and phones.
    2. Call the create_contact service to create both contacts.
    3. Call the get_contacts service to retrieve the list of contacts.
    4. Assert that the list contains at least two contacts.
    """
    contact_data1 = ContactCreate(name="Alice", email="alice@example.com", phone="+111111111")
    contact_data2 = ContactCreate(name="Bob", email="bob@example.com", phone="+222222222")
    create_contact(db, contact_data1)
    create_contact(db, contact_data2)
    contacts = get_contacts(db)
    assert len(contacts) >= 2

def test_update_contact(db):
    """
    Test updating an existing contact.

    Steps:
    1. Create a ContactCreate object with name, email, and phone.
    2. Call the create_contact service to create the contact.
    3. Create another ContactCreate object with updated name, email, and phone.
    4. Call the update_contact service with the created contact's ID and the updated ContactCreate object.
    5. Assert that the updated contact has the correct updated name, email, and phone.
    """
    contact_data = ContactCreate(name="Charlie", email="charlie@example.com", phone="+333333333")
    created_contact = create_contact(db, contact_data)
    updated_data = ContactCreate(name="Charlie Updated", email="charlie.updated@example.com", phone="+444444444")
    updated_contact = update_contact(db, created_contact.id, updated_data)
    assert updated_contact.name == "Charlie Updated"
    assert updated_contact.email == "charlie.updated@example.com"
    assert updated_contact.phone == "+444444444"

def test_delete_contact(db):
    """
    Test deleting a contact.

    Steps:
    1. Create a ContactCreate object with name, email, and phone.
    2. Call the create_contact service to create the contact.
    3. Call the delete_contact service with the created contact's ID.
    4. Assert that the deleted contact has the correct ID.
    5. Call the get_contact service with the deleted contact's ID and assert that it returns None.
    """
    contact_data = ContactCreate(name="Dave", email="dave@example.com", phone="+555555555")
    created_contact = create_contact(db, contact_data)
    deleted_contact = delete_contact(db, created_contact.id)
    assert deleted_contact.id == created_contact.id
    assert get_contact(db, created_contact.id) is None