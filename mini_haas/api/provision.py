"""Provision runner endpoint."""

from flask import Blueprint, jsonify

from ..services import provision

bp = Blueprint("provision", __name__)


@bp.post("/provision/run-once")
def run_once():
    result = provision.run_once()
    return jsonify(result)
