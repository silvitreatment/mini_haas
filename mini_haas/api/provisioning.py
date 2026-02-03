"""Provisioning endpoints."""

from flask import Blueprint, jsonify, request

bp = Blueprint("provisioning", __name__)


@bp.get("/provision/jobs")
def list_jobs():
    _ = request.args
    return jsonify({"error": "not_implemented"}), 501


@bp.post("/provision/jobs/<int:job_id>/retry")
def retry_job(job_id: int):
    return jsonify({"error": "not_implemented", "id": job_id}), 501
