"""Datacenter endpoints."""

from flask import Blueprint, jsonify, request

from ..services import datacenters

bp = Blueprint("datacenters", __name__)


@bp.post("/datacenters")
def create_datacenter():
    payload = request.get_json(silent=True) or {}
    dc = datacenters.create_datacenter(payload)
    return jsonify(dc), 201
