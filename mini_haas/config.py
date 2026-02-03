"""Application configuration."""

import os


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


class BaseConfig:
    ENV = _env("FLASK_ENV", "production")
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = _env(
        "DATABASE_URL",
        "postgresql+psycopg://mini_haas:mini_haas@localhost:5432/mini_haas",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Worker cadence and retry defaults
    PROVISION_POLL_SECONDS = int(_env("PROVISION_POLL_SECONDS", "5"))
    PROVISION_MAX_ATTEMPTS = int(_env("PROVISION_MAX_ATTEMPTS", "3"))


class DevConfig(BaseConfig):
    ENV = "development"
    DEBUG = True


class TestConfig(BaseConfig):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = _env(
        "DATABASE_URL",
        "postgresql+psycopg://mini_haas:mini_haas@localhost:5432/mini_haas_test",
    )
