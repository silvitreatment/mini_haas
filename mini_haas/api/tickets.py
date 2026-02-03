"""Ticket endpoints."""

from flask import Blueprint, jsonify, request

bp = Blueprint("tickets", __name__)


@bp.get("/tickets")
def list_tickets():
    _ = request.args
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/tickets/<int:ticket_id>/status")
def update_ticket(ticket_id: int):
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented", "id": ticket_id}), 501
