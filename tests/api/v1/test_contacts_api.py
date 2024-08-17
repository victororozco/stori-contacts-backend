from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

def test_create_contact(client: TestClient):
    """
    Test the creation of a new contact.

    Steps:
    1. Send a POST request to create a new contact with name, email, and phone.
    2. Assert that the response status code is 200.
    3. Assert that the response contains the correct name and an ID.
    """
    response = client.post(
        f"{settings.API_V1_STR}/contacts/",
        json={"name": "Test User", "email": "test@example.com", "phone": "1234567890"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data

def test_read_contacts(client: TestClient, test_db: Session):
    """
    Test retrieving the list of contacts.

    Steps:
    1. Create a new contact by sending a POST request.
    2. Send a GET request to retrieve the list of contacts.
    3. Assert that the response status code is 200.
    4. Assert that the response contains at least one contact.
    """
    client.post(
        f"{settings.API_V1_STR}/contacts/",
        json={"name": "Test User", "email": "test@example.com", "phone": "1234567890"}
    )
    
    response = client.get(f"{settings.API_V1_STR}/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_contact(client: TestClient, test_db: Session):
    """
    Test retrieving a specific contact by ID.

    Steps:
    1. Create a new contact by sending a POST request.
    2. Send a GET request to retrieve the contact by its ID.
    3. Assert that the response status code is 200.
    4. Assert that the response contains the correct name.
    """
    create_response = client.post(
        f"{settings.API_V1_STR}/contacts/",
        json={"name": "Test User", "email": "test@example.com", "phone": "1234567890"}
    )
    create_data = create_response.json()
    
    response = client.get(f"{settings.API_V1_STR}/contacts/{create_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"

def test_update_contact(client: TestClient, test_db: Session):
    """
    Test updating an existing contact.

    Steps:
    1. Create a new contact by sending a POST request.
    2. Send a PUT request to update the contact's name, email, and phone.
    3. Assert that the response status code is 200.
    4. Assert that the response contains the updated name.
    """
    create_response = client.post(
        f"{settings.API_V1_STR}/contacts/",
        json={"name": "Test User", "email": "test@example.com", "phone": "1234567890"}
    )
    create_data = create_response.json()
    
    response = client.put(
        f"{settings.API_V1_STR}/contacts/{create_data['id']}",
        json={"name": "Updated User", "email": "updated@example.com", "phone": "9876543210"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User"

def test_delete_contact(client: TestClient, test_db: Session):
    """
    Test deleting a contact.

    Steps:
    1. Create a new contact by sending a POST request.
    2. Send a DELETE request to delete the contact by its ID.
    3. Assert that the response status code is 200.
    4. Send a GET request to verify that the contact no longer exists.
    5. Assert that the response status code is 404.
    """
    create_response = client.post(
        f"{settings.API_V1_STR}/contacts/",
        json={"name": "Test User", "email": "test@example.com", "phone": "1234567890"}
    )
    create_data = create_response.json()
    
    response = client.delete(f"{settings.API_V1_STR}/contacts/{create_data['id']}")
    assert response.status_code == 200
    
    # Verify that the contact was deleted
    get_response = client.get(f"{settings.API_V1_STR}/contacts/{create_data['id']}")
    assert get_response.status_code == 404