from typing import Optional

from pydantic import (
    BaseSettings,
)


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: str = "6379"
    cache_dsn: Optional[str]

    CACHE_EXPIRE_IN_SECONDS: int = 300

    def __init__(self, **data):
        super(RedisSettings, self).__init__(**data)
        self.cache_dsn = f"redis://{self.host}:{self.port}/0"

    class Config:
        env_prefix = "REDIS_"
        env_file = ".env"
        env_file_encoding = "utf-8"
