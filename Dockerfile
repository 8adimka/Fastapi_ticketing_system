FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml ./

# Устанавливаем зависимости (poetry.lock может отсутствовать при первом запуске)
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root

# Копируем исходный код
COPY . .

# Устанавливаем PYTHONPATH для корректного импорта модулей
ENV PYTHONPATH=/app/src

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["./entrypoint.sh"]
