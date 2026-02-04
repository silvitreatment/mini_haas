"""Provision runner service."""

from __future__ import annotations

import random
from typing import Any

from sqlalchemy import select

from ..extensions import db
from ..models import Order, ProvisionJob, Server
from ..models.enums import OrderStatus, ProvisionStatus, ServerState


def run_once() -> dict[str, Any]:
    with db.session.begin():
        job = (
            db.session.execute(
                select(ProvisionJob)
                .where(ProvisionJob.status == ProvisionStatus.PENDING)
                .order_by(ProvisionJob.id.asc())
                .with_for_update(skip_locked=True)
            )
            .scalars()
            .first()
        )
        if not job:
            return {"status": "no_jobs"}

        job.status = ProvisionStatus.RUNNING
        job.attempt += 1

        server = db.session.get(Server, job.server_id)
        order = db.session.get(Order, job.order_id)

        success = random.random() < 0.9
        if success:
            job.status = ProvisionStatus.SUCCESS
            server.state = ServerState.IN_SERVICE
        else:
            job.status = ProvisionStatus.FAILED
            job.last_error = "simulated failure"
            server.state = ServerState.BROKEN

        order_jobs = (
            db.session.execute(
                select(ProvisionJob).where(ProvisionJob.order_id == order.id)
            )
            .scalars()
            .all()
        )
        if any(j.status == ProvisionStatus.FAILED for j in order_jobs):
            order.status = OrderStatus.FAILED
        elif all(j.status == ProvisionStatus.SUCCESS for j in order_jobs):
            order.status = OrderStatus.ACTIVE

        return {
            "job_id": job.id,
            "order_id": job.order_id,
            "server_id": job.server_id,
            "status": job.status.value,
        }
