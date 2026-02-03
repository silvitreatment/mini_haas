"""Telemetry endpoints."""

from flask import Blueprint, jsonify, request

bp = Blueprint("telemetry", __name__)


@bp.post("/telemetry")
def ingest_telemetry():
    _ = request.get_json(silent=True) or []
    return jsonify({"error": "not_implemented"}), 501
