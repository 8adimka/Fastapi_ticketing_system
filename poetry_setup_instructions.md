# Миграция с Pipenv на Poetry

## Установка Poetry

Если Poetry еще не установлен:

```bash
# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Или через pip (не рекомендуется, но работает)
pip install poetry
```

## Настройка Poetry

Настройте Poetry для создания виртуального окружения в папке проекта:

```bash
poetry config virtualenvs.in-project true
```

Это создаст папку `.venv` внутри проекта вместо глобального расположения.

## Инициализация и установка зависимостей

```bash
# Установите все зависимости (production + development)
poetry install

# Только production зависимости
poetry install --only main

# Установить development зависимости
poetry install --with dev

# Обновите зависимости (если нужно)
poetry update
```

## Работа с проектом

```bash
# Активировать виртуальное окружение
poetry shell

# Запустить команду внутри виртуального окружения (без активации)
poetry run python src/main.py

# Добавить новую зависимость
poetry add package_name

# Добавить development зависимость
poetry add --dev package_name

# Удалить зависимость
poetry remove package_name

# Показать информацию о зависимостях
poetry show
poetry show --tree
```

## Важные команды

```bash
# Проверить корректность pyproject.toml
poetry check

# Экспорт в requirements.txt (если нужно)
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --output requirements-dev.txt --dev

# Сборка пакета
poetry build

# Публикация в PyPI
poetry publish
```

## Структура проекта после миграции

```
selectel_ticketing_system/
├── .venv/                 # Виртуальное окружение (создастся автоматически)
├── pyproject.toml         # Файл конфигурации Poetry
├── poetry.lock           # Файл блокировки версий (создастся автоматически)
├── src/                  # Исходный код
└── README.md
```

## Особенности миграции

1. **Все зависимости перенесены** из Pipfile в pyproject.toml с сохранением версий
2. **Разделение зависимостей**: production в `[project.dependencies]`, development в `[project.optional-dependencies.dev]`
3. **Виртуальное окружение** будет создано в папке `.venv` внутри проекта
4. **Poetry.lock** заменит Pipfile.lock для гарантии воспроизводимости сборок
5. **Современный формат**: Используется новый синтаксис Poetry 1.2+ с секцией `[project]`

## Проверка миграции

После установки проверьте, что все работает:

```bash
poetry run python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
poetry run python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"
```

## Решение возможных проблем

Если возникнут конфликты версий:

```bash
# Очистить кэш Poetry
poetry cache clear --all .

# Переустановить зависимости
poetry install
```

Для обратной совместимости можно сохранить requirements.txt:

```bash
poetry export -f requirements.txt --output requirements.txt
