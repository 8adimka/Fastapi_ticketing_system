from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: str = "6379"
    CACHE_EXPIRE_IN_SECONDS: int = 300

    @computed_field
    @property
    def cache_dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/0"

    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=None)
