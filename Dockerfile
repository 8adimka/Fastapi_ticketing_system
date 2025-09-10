FROM python:3.9-slim

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копируем исходный код
COPY . .

# Создаем папки для данных если их нет
RUN mkdir -p data redis_data

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["./entrypoint.sh"]
