from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class DBSettings(BaseSettings):
    pg_dsn: PostgresDsn = (
        "postgresql://tickets:test@postgres_sql:5432/tickets_system_db"  # type: ignore
    )

    class Config:
        env_prefix = "DATABASE_"
        env_file = ".env"
        env_file_encoding = "utf-8"
