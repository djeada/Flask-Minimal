"""
Configuration settings for the Flask application.
"""

import os
from typing import Optional, Type


class Config:
    """Base configuration class."""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = False
    TESTING = False

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///library.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Security settings
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY") or "jwt-secret-change-in-production"
    )
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(
        os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24)
    )
    BCRYPT_LOG_ROUNDS = int(os.environ.get("BCRYPT_LOG_ROUNDS", 12))

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"

    # Pagination
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 20))
    MAX_ITEMS_PER_PAGE = int(os.environ.get("MAX_ITEMS_PER_PAGE", 100))


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or "sqlite:///library_dev.db"
    )
    BCRYPT_LOG_ROUNDS = 4  # Faster hashing for development


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    BCRYPT_LOG_ROUNDS = 4  # Faster hashing for tests
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "postgresql://user:password@localhost/library"
    )

    # Security enhancements for production
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name: Optional[str] = None) -> Type[Config]:
    """Get configuration class based on environment."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")
    return config[config_name]
