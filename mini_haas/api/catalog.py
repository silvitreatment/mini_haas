"""Catalog and stock endpoints."""

from flask import Blueprint, jsonify, request

bp = Blueprint("catalog", __name__)


@bp.post("/server-models")
def create_server_model():
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/firmwares")
def create_firmware():
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/firmware-profiles")
def create_firmware_profile():
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/os-images")
def create_os_image():
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/warehouse-stock/add")
def add_warehouse_stock():
    _ = request.get_json(silent=True) or {}
    return jsonify({"error": "not_implemented"}), 501
