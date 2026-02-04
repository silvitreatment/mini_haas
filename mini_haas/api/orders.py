"""Order endpoints."""

from flask import Blueprint, jsonify, request

from ..services import orders

bp = Blueprint("orders", __name__)


@bp.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    order = orders.create_order(payload)
    return jsonify(order), 201


@bp.post("/orders/<int:order_id>/allocate")
def allocate(order_id: int):
    result = orders.allocate_order(order_id)
    return jsonify(result)


@bp.post("/orders/<int:order_id>/provision")
def provision(order_id: int):
    result = orders.provision_order(order_id)
    return jsonify(result)


@bp.get("/orders/<int:order_id>")
def get_order(order_id: int):
    order = orders.get_order(order_id)
    return jsonify(order)
