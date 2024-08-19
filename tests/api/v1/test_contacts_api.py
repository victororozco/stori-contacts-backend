import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.schemas.contact import ContactCreate

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a TestClient instance for making requests to the FastAPI app
client = TestClient(app)

# Fixture to provide a sample contact for tests
@pytest.fixture
def sample_contact():
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "address": "123 Main St"
    }

# Test creating a new contact
def test_create_contact(sample_contact):
    response = client.post("/api/v1/contacts/", json=sample_contact)
    assert response.status_code == 201  # Check if the response status code is 201 (Created)
    data = response.json()
    assert data["name"] == sample_contact["name"]  # Verify the name in the response
    assert data["email"] == sample_contact["email"]  # Verify the email in the response
    assert "id" in data  # Check if the response contains an id

# Test creating a contact with a duplicate email
def test_create_contact_duplicate_email(sample_contact):
    client.post("/api/v1/contacts/", json=sample_contact)
    response = client.post("/api/v1/contacts/", json=sample_contact)
    assert response.status_code == 400  # Check if the response status code is 400 (Bad Request)

# Test reading all contacts
def test_read_contacts():
    response = client.get("/api/v1/contacts/")
    assert response.status_code == 200  # Check if the response status code is 200 (OK)
    assert isinstance(response.json(), list)  # Verify the response is a list

# Test reading a specific contact by ID
def test_read_contact(sample_contact):
    create_response = client.post("/api/v1/contacts/", json=sample_contact)
    contact_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/contacts/{contact_id}")
    assert response.status_code == 200  # Check if the response status code is 200 (OK)
    assert response.json()["name"] == sample_contact["name"]  # Verify the name in the response

# Test reading a contact that does not exist
def test_read_contact_not_found():
    response = client.get("/api/v1/contacts/9999")
    assert response.status_code == 404  # Check if the response status code is 404 (Not Found)

# Test updating a contact
def test_update_contact(sample_contact):
    create_response = client.post("/api/v1/contacts/", json=sample_contact)
    contact_id = create_response.json()["id"]
    
    updated_data = sample_contact.copy()
    updated_data["name"] = "Jane Doe"
    
    response = client.put(f"/api/v1/contacts/{contact_id}", json=updated_data)
    assert response.status_code == 200  # Check if the response status code is 200 (OK)
    assert response.json()["name"] == "Jane Doe"  # Verify the updated name in the response

# Test deleting a contact
def test_delete_contact(sample_contact):
    create_response = client.post("/api/v1/contacts/", json=sample_contact)
    contact_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/contacts/{contact_id}")
    assert response.status_code == 200  # Check if the response status code is 200 (OK)
    
    # Verify the contact was deleted
    get_response = client.get(f"/api/v1/contacts/{contact_id}")
    assert get_response.status_code == 404  # Check if the response status code is 404 (Not Found)

# Test deleting a contact that does not exist
def test_delete_contact_not_found():
    response = client.delete("/api/v1/contacts/9999")
    assert response.status_code == 404  # Check if the response status code is 404 (Not Found)