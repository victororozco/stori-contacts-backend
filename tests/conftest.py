import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_db_engine():
    """
    Create a SQLAlchemy engine for the test database.
    
    Steps:
    1. Create an engine connected to the in-memory SQLite database.
    2. Create all tables defined in the Base metadata.
    3. Yield the engine to be used in tests.
    4. Drop all tables after the tests are done.
    """
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)  # Create tables
    yield engine
    Base.metadata.drop_all(bind=engine)  # Drop tables after all tests

@pytest.fixture(scope="function")
def test_db(test_db_engine):
    """
    Create a new database session for a test.

    Steps:
    1. Connect to the test database engine.
    2. Begin a new transaction.
    3. Create a new session bound to the connection.
    4. Yield the session to be used in tests.
    5. Rollback the transaction and close the connection after the test.
    """
    connection = test_db_engine.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = TestingSessionLocal()
    
    yield db
    
    db.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(test_db):
    """
    Create a new TestClient for the FastAPI app.

    Steps:
    1. Override the get_db dependency to use the test database session.
    2. Create a TestClient instance for the FastAPI app.
    3. Yield the TestClient to be used in tests.
    4. Remove the dependency override after the test.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    del app.dependency_overrides[get_db]

@pytest.fixture(scope="session", autouse=True)
def override_settings():
    """
    Override the settings for the test session.

    Steps:
    1. Set the DATABASE_URL in the settings to use the test database URL.
    """
    settings.DATABASE_URL = TEST_DATABASE_URL