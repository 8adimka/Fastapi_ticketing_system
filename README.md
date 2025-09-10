# Ticketing System API

## Содержание

1. [Описание проекта](#описание)
2. [Используемые технологии](#используемые-технологии)
3. [Структура проекта](#структура-проекта)
4. [Работа с проектом](#работа-с-проектом)
    - 4.1 [Запуск проекта](#запуск-проекта)
        - [Переменные окружения](#переменные-окружения)
    - 4.2 [Настройка виртуального окружения](#настройка-виртуального-окружения)
    - 4.3 [Переменные окружения](#переменные-окружения)
    - 4.4 [Управление миграциями через Alembic](#управление-миграциями-через-alembic)
5. [Инструкция по тестированию Ticketing System API](#инструкция-по-тестированию-ticketing-system-api)
6. [Полезные материалы](#полезные-материалы)

## Описание

### Тикет-система

Тикет-система должна состоять из:  

- Тикетов, у тикетов могут быть комментарии
- Тикет создается в статусе “открыт”, может перейти в “отвечен” или “закрыт”, из  
отвечен в “ожидает ответа” или “закрыт”, статус “закрыт” финальный (нельзя  
изменить статус или добавить комментарий)  

## Используемые технологии

- Код приложения пишется на **Python + FastAPI**.
- Приложение запускается под управлением сервера **ASGI**(uvicorn).
- Хранилище – **PostgreSQL**.
- За кеширование данных отвечает – **redis cluster**.

## Структура проекта

- Корень проекта — в нём находятся базовые вещи, например, ci и gitignore.
- `src` — содержит исходный код приложения.
- `main.py` — входная точка приложения.
- `api` — модуль, в котором реализуется API. Другими словами,
  это модуль для предоставления http-интерфейса клиентским приложениям.
  Внутри модуля отсутствует какая-либо бизнес-логика, так как она не должна быть завязана на HTTP.
- `core` — содержит разные конфигурационные файлы.
- `db` — предоставляет объекты баз данных (Redis, PostgreSQL) и провайдеры для внедрения зависимостей.
  Redis будет использоваться для кеширования, чтобы не нагружать лишний раз PostgreSQL.
- `models` — содержит классы, описывающие бизнес-сущности
- `schemas` - содержит модели отвечающие за валидацию тела запроса.
- `services` — главное в сервисе. В этом модуле находится реализация всей бизнес-логики.
  Благодаря такому разделению,  будет легче добавлять новые типы в сервис.

## Работа с проектом

### Запуск проекта

Проект полностью контейнеризован и запускается одной командой:

```bash
docker-compose up --build
```

Эта команда:

1. Соберет Docker-образ приложения
2. Запустит PostgreSQL, Redis и само приложение
3. Healthchecks обеспечат правильный порядок запуска
4. Приложение автоматически применит миграции и запустится

После запуска приложение будет доступно по адресу: <http://localhost:8000>

Документация API:

- Swagger UI: <http://localhost:8000/api/openapi>
- ReDoc: <http://localhost:8000/api/redoc>

#### Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл при необходимости.

```dotenv
DATABASE_DSN='<строка подключения к Database>'
REDIS_HOST='<адрес Redis хоста>'
REDIS_PORT='<порт для подключения к Redis>'
```

### Настройка виртуального окружения

Проект использует Poetry для управления зависимостями. Установите Poetry если еще не установлен:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Или через pip:

```bash
pip install poetry
```

Установите зависимости:

```bash
poetry install
```

Активируйте виртуальное окружение:

```bash
poetry shell
```

### Управление миграциями через Alembic

**Данные операции необходимо выполнять из директории `src`**

1. Создание миграций (используя Poetry):

   ```bash
   poetry run alembic -c ./models/alembic.ini revision -m "some message" --autogenerate
   ```

   Данная команда сгенерирует новую миграцию, но не применит её к БД.

2. Применение миграции к БД:

   ```bash
   poetry run alembic -c ./models/alembic.ini upgrade head
   ```

### Инструкция по тестированию Ticketing System API

#### 🔗 Базовый URL: `http://localhost:8000`

#### 📚 Документация

- **Swagger UI**: [](http://localhost:8000/api/openapi)<http://localhost:8000/api/openapi>
- **ReDoc**: [](http://localhost:8000/api/redoc)<http://localhost:8000/api/redoc>

#### 🎯 Основные операции

##### 1. Получить список всех тикетов

```bash
curl -X GET "http://localhost:8000/v1/ticket/" \
  -H "Content-Type: application/json"
```

##### 2. Создать новый тикет

```bash
curl -X POST "http://localhost:8000/v1/ticket/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Проблема с подключением",
    "description": "Не могу подключиться к серверу",
    "email": "user@example.com",
    "created_by": "Иван Иванов",
    "status": "open"
  }'
```

##### 3. Получить конкретный тикет (замените {ticket_id})

```bash
curl -X GET "http://localhost:8000/v1/ticket/{ticket_id}" \
  -H "Content-Type: application/json"
```

##### 4. Обновить статус тикета

```bash
curl -X PUT "http://localhost:8000/v1/ticket/{ticket_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "answered",
    "updated_by": "Администратор"
  }'
```

##### 5. Удалить тикет

```bash
curl -X DELETE "http://localhost:8000/v1/ticket/{ticket_id}" \
  -H "Content-Type: application/json"
```

#### 📊 Статусы тикетов

- `open` - открыт
- `answered` - отвечен
- `wait_answer` - ожидает ответа
- `closed` - закрыт (финальный)

#### 🔄 Правила смены статусов

- Из `open` → `answered` или `closed`
- Из `answered` → `wait_answer` или `closed`
- Из `closed` - нельзя изменить статус или добавить комментарий

## Тестирование

Проект использует pytest для модульного тестирования. Тесты расположены в директории `tests/`.

### Запуск тестов

```bash
# Запуск всех тестов с покрытием
poetry run python -m pytest tests/ --cov=src --cov-report=term-missing

# Запуск конкретного модуля тестов
poetry run python -m pytest tests/unit/core/ --cov=src

# Запуск с детальным выводом
poetry run python -m pytest tests/ -v
```

### Структура тестов

```
tests/
├── unit/                 # Модульные тесты
│   ├── core/            # Тесты ядра приложения
│   │   ├── test_config_settings.py
│   │   ├── test_exceptions.py
│   │   ├── test_logger.py
│   │   └── test_modules.py
│   ├── models/          # Тесты моделей
│   │   └── test_base_mixins.py
│   ├── schemas/         # Тесты схем
│   └── api/             # Тесты API
└── integration/         # Интеграционные тесты
```

Тесты покрывают все ключевые модули

## Переменные окружения (актуальные)

Файл `.env` должен содержать следующие переменные:

```dotenv
# Для Docker совместимости
PG_USER=tickets
PG_PASSWD=test
PG_DB_NAME=tickets_system_db

# Для приложения (с префиксами)
DATABASE_PG_USER=tickets
DATABASE_PG_PASSWORD=test
DATABASE_PG_DB_NAME=tickets_system_db
```

## Полезные материалы

[Пишем и тестируем миграции БД с Alembic](https://habr.com/ru/company/yandex/blog/511892/)  
[Poetry: документация](https://python-poetry.org/docs/)  
[FastAPI документация](https://fastapi.tiangolo.com/)  
[Pydantic v2 документация](https://docs.pydantic.dev/latest/)
