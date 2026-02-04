"""API blueprints."""

from flask import Flask

from .errors import register_error_handlers
from .inventory import bp as inventory_bp
from .models import bp as models_bp
from .orders import bp as orders_bp
from .provision import bp as provision_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(inventory_bp)
    app.register_blueprint(models_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(provision_bp)
    register_error_handlers(app)
