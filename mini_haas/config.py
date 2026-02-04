"""App configuration."""

import os


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


class Config:
    SQLALCHEMY_DATABASE_URI = _env(
        "DATABASE_URL",
        "postgresql+psycopg://mini_haas:mini_haas@localhost:5432/mini_haas",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
