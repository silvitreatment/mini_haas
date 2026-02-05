from __future__ import annotations

import os

import pytest

from mini_haas.app import create_app
from mini_haas.extensions import db


def _get_test_db_url() -> str:
    url = os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL not set for tests")
    if url.startswith("sqlite"):
        pytest.skip("SQLite does not support FOR UPDATE SKIP LOCKED")
    return url


@pytest.fixture(scope="session")
def app():
    class TestConfig:
        SQLALCHEMY_DATABASE_URI = _get_test_db_url()
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        TESTING = True

    app = create_app(TestConfig)
    return app


@pytest.fixture()
def db_session(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app, db_session):
    return app.test_client()
