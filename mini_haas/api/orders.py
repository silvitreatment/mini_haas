"""Order endpoints."""

from flask import Blueprint, jsonify, request

bp = Blueprint("orders", __name__)


@bp.post("/orders")
def create_order():
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/orders/<int:order_id>/plan")
def plan_order(order_id: int):
    return jsonify({"error": "not_implemented", "id": order_id}), 501


@bp.post("/orders/<int:order_id>/allocate")
def allocate_order(order_id: int):
    return jsonify({"error": "not_implemented", "id": order_id}), 501


@bp.post("/orders/<int:order_id>/provision")
def provision_order(order_id: int):
    return jsonify({"error": "not_implemented", "id": order_id}), 501


@bp.get("/orders/<int:order_id>")
def get_order(order_id: int):
    return jsonify({"error": "not_implemented", "id": order_id}), 501
