# Stori Contacts Backend

This project is a FastAPI-based backend for managing contacts.

## Features

- CRUD operations for contacts
- PostgreSQL database integration
- Alembic for database migrations
- Docker support 
- Pytest for unit testing

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (if running locally without Docker)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/victororozco/stori-contacts-backend.git
   cd stori-contacts-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your environment variables (example):
    ```
    PROJECT_NAME=Contacts App
    API_V1_STR=/api/v1
    POSTGRES_USER=stori_user
    POSTGRES_PASSWORD=stori_password
    POSTGRES_DB=stori_db
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    API_PORT=8000
    ```

## Running the Application

### Using Docker

1. Build and start the containers:
   ```
   docker compose up --build
   ```

2. Run the database migrations:
   ```
   docker compose run web alembic upgrade head
   ```

3. The API will be available at `http://localhost:8000`

4. To create a new migration:
    ```docker
    docker compose run web alembic revision --autogenerate -m "Description of changes"
    ```

5. To downgrade:
    ```
    docker-compose run web alembic downgrade -1
    ```

### Without Docker

1. Ensure you have a PostgreSQL server running and accessible.

2. Run the database migrations:
   ```
   alembic upgrade head
   ```

3. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

4. The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access the automatic interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`

## Running Tests

To run the tests, execute:

### With docker
```
docker compose run web pytest -v
```

### Without docker
```
pytest -v
```

## Project Structure

```
stori-contacts-backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── tests/
├── alembic/
├── docker compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```