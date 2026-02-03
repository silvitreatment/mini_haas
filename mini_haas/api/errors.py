"""API error handlers."""

from flask import Flask, jsonify

from ..services.errors import ServiceError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ServiceError)
    def handle_service_error(error: ServiceError):
        return jsonify({"error": str(error)}), error.status_code
