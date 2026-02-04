"""Inventory endpoints."""

from flask import Blueprint, jsonify, request

from ..services import inventory

bp = Blueprint("inventory", __name__)


@bp.post("/servers")
def create_server():
    payload = request.get_json(silent=True) or {}
    server = inventory.create_server(payload)
    return jsonify(server), 201


@bp.get("/servers")
def list_servers():
    servers = inventory.list_servers(request.args)
    return jsonify(servers)
