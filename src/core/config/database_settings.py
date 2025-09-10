from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    pg_host: str = "postgres_sql"
    pg_port: int = 5432
    pg_user: str = "tickets"
    pg_password: str = "test"
    pg_db_name: str = "tickets_system_db"

    @computed_field
    @property
    def pg_dsn(self) -> str:
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db_name}"

    model_config = SettingsConfigDict(env_prefix="DATABASE_", env_file=None)
