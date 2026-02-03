"""API blueprints."""

from flask import Flask

from .catalog import bp as catalog_bp
from .errors import register_error_handlers
from .inventory import bp as inventory_bp
from .orders import bp as orders_bp
from .provisioning import bp as provisioning_bp
from .telemetry import bp as telemetry_bp
from .tickets import bp as tickets_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(inventory_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(provisioning_bp)
    app.register_blueprint(telemetry_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(catalog_bp)
    register_error_handlers(app)
