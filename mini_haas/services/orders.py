"""Order service: create, allocate, provision."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select

from ..extensions import db
from ..models import Datacenter, Order, OrderItem, ProvisionJob, Server, ServerModel
from ..models.enums import OrderStatus, ProvisionStatus, ServerState
from .errors import ConflictError, NotFoundError, ValidationError


def _parse_positive_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def _parse_positive_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def create_order(_payload: dict[str, Any]):
    name = (_payload.get("datacenter") or "").strip()
    cpu = _parse_positive_int(_payload.get("cpu_cores"))
    ram = _parse_positive_int(_payload.get("ram_gb"))
    nvme = _parse_positive_number(_payload.get("nvme_tb"))

    if not name or cpu is None or ram is None or nvme is None:
        raise ValidationError("Invalid payload")

    datacenter = db.session.execute(
        select(Datacenter).where(Datacenter.name == name)
    ).scalar_one_or_none()
    if not datacenter:
        raise NotFoundError("datacenter not found")

    order = Order(
        datacenter_id=datacenter.id,
        requested_cpu_cores=cpu,
        requested_ram_gb=ram,
        requested_nvme_tb=nvme,
    )
    db.session.add(order)
    db.session.commit()

    return {
        "id": order.id,
        "datacenter": datacenter.name,
        "requested": {
            "cpu_cores": order.requested_cpu_cores,
            "ram_gb": order.requested_ram_gb,
            "nvme_tb": float(order.requested_nvme_tb),
        },
        "status": order.status.value,
    }


def allocate_order(order_id: int):
    order = db.session.get(Order, order_id)
    
    if not order:
        raise NotFoundError("order not found")
    if order.status != OrderStatus.NEW:
        raise ConflictError("order not in correct status")
    
    candidates = (
        db.session.execute(
            select(Server)
            .join(Server.model)
            .where(
                Server.state == ServerState.AVAILABLE,
                Server.datacenter_id == order.datacenter_id,
            )
            .order_by(
                ServerModel.cpu_cores.desc(),
                ServerModel.ram_gb.desc(),
                ServerModel.nvme_tb.desc(),
            )
        )
        .scalars()
        .all()
    )
    
    picked = []
    cpu = ram = 0
    nvme = 0
    for srv in candidates:
        picked.append(srv)
        cpu += srv.model.cpu_cores
        nvme += float(srv.model.nvme_tb)
        ram += srv.model.ram_gb
        if cpu >= order.requested_cpu_cores and ram >= order.requested_ram_gb and nvme >= float(order.requested_nvme_tb):
            break
    if cpu < order.requested_cpu_cores or ram < order.requested_ram_gb or nvme < float(order.requested_nvme_tb):
        raise ConflictError("insufficient capacity")
    server_ids = [srv.id for srv in picked]
    with db.session.begin():
        
        servers = (
            db.session.execute(
                select(Server)
                .where(Server.id.in_(server_ids))
                .with_for_update()
            )
            .scalars()
            .all()
        )
        if any(s.state != ServerState.AVAILABLE for s in servers):
            raise ConflictError("capacity changed, replan required")
        
        for s in servers:
            s.state = ServerState.ALLOCATED
            s.allocated_order_id = order.id
            db.session.add(OrderItem(order_id=order_id, server_id=s.id))
        order.status = OrderStatus.ALLOCATED

    return {
        "order_id": order.id,
        "status": order.status.value,
        "servers": [s.barcode for s in servers],
    }


def provision_order(_order_id: int):
    order = db.session.get(Order, _order_id)
    if not order:
        raise NotFoundError("order not found")
    if order.status != OrderStatus.ALLOCATED:
        raise ConflictError("order not in correct status")

    server_ids = [item.server_id for item in order.items]
    if not server_ids:
        raise ConflictError("no servers allocated")

    with db.session.begin():
        servers = (
            db.session.execute(
                select(Server).where(Server.id.in_(server_ids)).with_for_update()
            )
            .scalars()
            .all()
        )
        for server in servers:
            db.session.add(
                ProvisionJob(
                    order_id=order.id,
                    server_id=server.id,
                    status=ProvisionStatus.PENDING,
                )
            )
            server.state = ServerState.PROVISIONING
        order.status = OrderStatus.PROVISIONING

    return {"order_id": order.id, "status": order.status.value}


def get_order(_order_id: int):
    order = db.session.get(Order, _order_id)
    if not order:
        raise NotFoundError("order not found")

    servers = [item.server.barcode for item in order.items]
    jobs = [
        {"server": job.server.barcode, "status": job.status.value}
        for job in order.provision_jobs
    ]

    return {
        "id": order.id,
        "datacenter": order.datacenter.name,
        "requested": {
            "cpu_cores": order.requested_cpu_cores,
            "ram_gb": order.requested_ram_gb,
            "nvme_tb": float(order.requested_nvme_tb),
        },
        "status": order.status.value,
        "servers": servers,
        "provision_jobs": jobs,
    }
