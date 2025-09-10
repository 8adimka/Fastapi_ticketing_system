from src.core.config.database_settings import DBSettings
from src.core.config.redis_settings import RedisSettings


class TestConfigSimple:
    """Test cases for configuration settings without AppSettings"""

    def test_db_settings_defaults(self):
        """Test DBSettings default values"""
        # Create DBSettings with empty environment to avoid conflicts
        db_settings = DBSettings.model_construct()

        assert db_settings.pg_host == "postgres_sql"
        assert db_settings.pg_port == 5432
        assert db_settings.pg_user == "tickets"
        assert db_settings.pg_password == "test"
        assert db_settings.pg_db_name == "tickets_system_db"
        assert (
            db_settings.pg_dsn
            == "postgresql://tickets:test@postgres_sql:5432/tickets_system_db"
        )

    def test_redis_settings_defaults(self):
        """Test RedisSettings default values"""
        # Create RedisSettings with empty environment to avoid conflicts
        redis_settings = RedisSettings.model_construct()

        assert redis_settings.host == "redis"
        assert redis_settings.port == "6379"
        assert redis_settings.CACHE_EXPIRE_IN_SECONDS == 300
        assert redis_settings.cache_dsn == "redis://redis:6379/0"

    def test_db_settings_custom_values(self):
        """Test DBSettings with custom values"""
        db_settings = DBSettings.model_construct(
            pg_host="localhost",
            pg_port=5433,
            pg_user="custom_user",
            pg_password="custom_pass",
            pg_db_name="custom_db",
        )

        assert (
            db_settings.pg_dsn
            == "postgresql://custom_user:custom_pass@localhost:5433/custom_db"
        )

    def test_redis_settings_custom_values(self):
        """Test RedisSettings with custom values"""
        redis_settings = RedisSettings.model_construct(host="localhost", port="6380")

        assert redis_settings.cache_dsn == "redis://localhost:6380/0"
