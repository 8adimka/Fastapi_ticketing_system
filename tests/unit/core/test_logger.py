from src.core.logger import LOGGING


class TestLogger:
    """Test cases for logger configuration"""

    def test_logging_config_structure(self):
        """Test that LOGGING configuration has correct structure"""
        assert isinstance(LOGGING, dict)
        assert "version" in LOGGING
        assert "formatters" in LOGGING
        assert "handlers" in LOGGING
        assert "loggers" in LOGGING
        assert "root" in LOGGING

    def test_logging_version(self):
        """Test logging version"""
        assert LOGGING["version"] == 1

    def test_logging_formatters(self):
        """Test logging formatters"""
        assert "default" in LOGGING["formatters"]
        assert "verbose" in LOGGING["formatters"]
        assert "access" in LOGGING["formatters"]

        verbose_formatter = LOGGING["formatters"]["verbose"]
        assert "format" in verbose_formatter
        assert (
            verbose_formatter["format"]
            == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        default_formatter = LOGGING["formatters"]["default"]
        assert "()" in default_formatter
        assert "fmt" in default_formatter

    def test_logging_handlers(self):
        """Test logging handlers"""
        assert "console" in LOGGING["handlers"]
        assert "default" in LOGGING["handlers"]
        assert "access" in LOGGING["handlers"]

        console_handler = LOGGING["handlers"]["console"]
        assert "class" in console_handler
        assert "formatter" in console_handler
        assert "level" in console_handler

    def test_logging_loggers(self):
        """Test logging loggers"""
        assert "" in LOGGING["loggers"]  # Root logger
        assert "uvicorn.access" in LOGGING["loggers"]
        assert "uvicorn.error" in LOGGING["loggers"]

        root_logger = LOGGING["loggers"][""]
        assert "handlers" in root_logger
        assert "level" in root_logger

        access_logger = LOGGING["loggers"]["uvicorn.access"]
        assert "handlers" in access_logger
        assert "level" in access_logger
        assert "propagate" in access_logger

    def test_logging_root_config(self):
        """Test root logger configuration"""
        root_config = LOGGING["root"]
        assert "handlers" in root_config
        assert "level" in root_config
