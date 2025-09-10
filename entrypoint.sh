#!/bin/sh

echo "Apply migrations"
poetry run alembic -c src/models/alembic.ini upgrade head

echo "Start API..."
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
