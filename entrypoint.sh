#!/bin/sh

# Создаем папки для данных с правильными правами
mkdir -p /app/data /app/redis_data
chmod 777 /app/data /app/redis_data

echo "Apply migrations"
cd /app && PYTHONPATH=/app/src poetry run alembic -c src/models/alembic.ini upgrade head || echo "Migrations failed or already applied"

echo "Start API..."
cd /app && PYTHONPATH=/app/src poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
