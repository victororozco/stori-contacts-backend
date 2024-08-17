#!/bin/sh

# Wait for the database to be ready
python /code/scripts/wait_for_db.py

# Run database migrations
alembic upgrade head

# Execute the command passed to the docker container
exec "$@"