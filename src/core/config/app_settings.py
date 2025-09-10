import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.config.database_settings import DBSettings
from src.core.config.redis_settings import RedisSettings


class AppSettings(BaseSettings):
    app_name: str = "Ticketing Service"
    app_version: str = "0.1.0"

    db: DBSettings
    redis_db: RedisSettings

    model_config = SettingsConfigDict(env_file=None)


# Функция для загрузки настроек с фильтрацией переменных окружения
def get_settings() -> AppSettings:
    # Загружаем переменные окружения из файла .env вручную
    env_vars = {}
    env_file_path = ".env"

    if os.path.exists(env_file_path):
        with open(env_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()

    # Фильтруем и преобразуем переменные для каждой подсистемы
    db_vars = {}
    redis_vars = {}

    for key, value in env_vars.items():
        if key.startswith("DATABASE_"):
            # Преобразуем DATABASE_PG_USER в pg_user
            field_name = key[
                9:
            ].lower()  # Убираем "DATABASE_" и приводим к нижнему регистру
            db_vars[field_name] = value
        elif key.startswith("REDIS_"):
            # Преобразуем REDIS_HOST в host
            field_name = key[
                6:
            ].lower()  # Убираем "REDIS_" и приводим к нижнему регистру
            redis_vars[field_name] = value

    # Создаем настройки с отфильтрованными переменными
    db_settings = DBSettings(**db_vars)
    redis_settings = RedisSettings(**redis_vars)

    return AppSettings(db=db_settings, redis_db=redis_settings)
