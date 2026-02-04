"""Order service: create, allocate, provision."""

from __future__ import annotations
from sqlalchemy import select
from sqlalchemy import Session 
from ..models import Order, OrderItem, Server, ServerModel
from ..models.enums import OrderStatus, ServerState

from typing import Any


def create_order(_payload: dict[str, Any]):
    raise NotImplementedError


def allocate_order(session : Session, order_id : int):
    """Transactional allocation using SELECT FOR UPDATE."""
    order = session.get(Order, order_id)
    
    if not order:
        raise "order not found"
    if order.status != OrderStatus.NEW:
        raise "order not in new status"
    
    candidates = (
        session.execute(
            select(Server)
            .join(Server.model)
            .where(
                Server.state == ServerState.AVAILABLE,
                Server.datacenter_id == order.datacentr_id,
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
        raise "insufficient capacity"
    with session.connect() as conn:
        
        servers = (
            session.execute(
                select(Server)
                .where(Server.id.in_(server_ids))
                .with_for_update()
            )
            .scalars()
            .all()
        )
        if any(s.state != ServerState.AVAILABLE for s in servers):
            raise "capacity changed, replan required"
        
        for s in servers:
            s.state = ServerState.ALLOCATED
            s.allocated_order_id = order.id 
            session.add(OrderItem(order_id=order_id, server_id = s.id))
    raise NotImplementedError


def provision_order(_order_id: int):
    """Create provision jobs and set PROVISIONING."""
    raise NotImplementedError


def get_order(_order_id: int):
    raise NotImplementedError
