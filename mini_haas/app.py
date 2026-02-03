"""Flask application factory."""

from flask import Flask

from . import models  # noqa: F401
from .api import register_blueprints
from .config import DevConfig
from .extensions import db, migrate


def create_app(config_object: str | object | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    return app
