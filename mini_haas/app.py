"""Flask application factory."""

from flask import Flask

from .api import register_blueprints
from .config import Config
from .extensions import db, migrate
from . import models  # noqa: F401


def create_app(config_object: object | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    return app
