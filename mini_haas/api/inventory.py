"""Inventory endpoints."""

from flask import Blueprint, jsonify, request

bp = Blueprint("inventory", __name__)


@bp.post("/scan")
def scan_server():
    """Scan barcode and place server into warehouse or rack."""
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501


@bp.get("/servers")
def list_servers():
    """List servers with optional filters."""
    return jsonify({"error": "not_implemented"}), 501


@bp.get("/servers/<int:server_id>")
def get_server(server_id: int):
    """Get server details by id."""
    return jsonify({"error": "not_implemented", "id": server_id}), 501
