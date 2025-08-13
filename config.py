"""Application configuration module.

This module provides configuration classes for different environments.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Base configuration class with common settings."""

    # Application settings
    SECRET_KEY: str = (
        os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    )

    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_RECORD_QUERIES: bool = True

    # API settings
    RESTX_VALIDATE: bool = True
    RESTX_MASK_SWAGGER: bool = False

    # Pagination
    QUOTES_PER_PAGE: int = 20
    MAX_QUOTES_PER_PAGE: int = 100

    # Static file settings
    BASE_DIR: Path = Path(__file__).parent.absolute()

    @staticmethod
    def init_app(app: Any) -> None:
        """Initialize application with this configuration."""
        pass


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG: bool = True
    TESTING: bool = False

    # Database
    SQLALCHEMY_DATABASE_URI: str = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{Config.BASE_DIR / 'futurama_quote_machine.db'}"
    )

    # Logging
    LOG_LEVEL: str = "DEBUG"
    LOG_TO_STDOUT: bool = True


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING: bool = True
    DEBUG: bool = False

    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

    # Disable CSRF tokens in the forms for testing
    WTF_CSRF_ENABLED: bool = False

    # Logging
    LOG_LEVEL: str = "WARNING"


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG: bool = False
    TESTING: bool = False

    # Database - Use environment variable with fallback
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL") or ""

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_STDOUT: bool = False

    @classmethod
    def init_app(cls, app: Any) -> None:
        """Initialize production-specific settings."""
        Config.init_app(app)

        # Validate required production settings
        if not app.config.get("SQLALCHEMY_DATABASE_URI"):
            raise ValueError(
                "DATABASE_URL environment variable must be set in production"
            )

        # Log to stderr in production
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


# Configuration mapping
config: Dict[str, type] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name: Optional[str] = None) -> type:
    """Get configuration class by name.

    Args:
        config_name: Name of the configuration to retrieve.
                    Defaults to FLASK_ENV environment variable or 'default'.

    Returns:
        Configuration class.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    return config.get(config_name, DevelopmentConfig)
