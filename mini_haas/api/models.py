"""Server model endpoints."""

from flask import Blueprint, jsonify, request

from ..services import catalog

bp = Blueprint("models", __name__)


@bp.post("/server-models")
def create_server_model():
    payload = request.get_json(silent=True) or {}
    model = catalog.create_server_model(payload)
    return jsonify(model), 201
