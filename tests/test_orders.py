from __future__ import annotations

from decimal import Decimal

import pytest

from mini_haas.extensions import db
from mini_haas.models import Datacenter, Order, OrderItem, ProvisionJob, Server, ServerModel
from mini_haas.models.enums import OrderStatus, ProvisionStatus, ServerState
from mini_haas.services.orders import allocate_order, create_order, get_order, provision_order
from mini_haas.services.provision import run_once
from mini_haas.services.errors import ConflictError


def _setup_inventory():
    dc = Datacenter(name="VLADIMIR")
    model = ServerModel(name="Dell-R740-64c-512g-4tb", cpu_cores=64, ram_gb=512, nvme_tb=Decimal("4.0"))
    servers = [
        Server(barcode="SRV-0001", datacenter=dc, model=model),
        Server(barcode="SRV-0002", datacenter=dc, model=model),
    ]
    db.session.add_all([dc, model, *servers])
    db.session.commit()
    return dc, model, servers


def test_allocate_creates_order_items(db_session):
    _setup_inventory()

    order_payload = {"datacenter": "VLADIMIR", "cpu_cores": 128, "ram_gb": 512, "nvme_tb": 6.0}
    order = create_order(order_payload)

    result = allocate_order(order["id"])
    assert result["status"] == OrderStatus.ALLOCATED.value

    stored = db.session.get(Order, order["id"])
    assert stored.status == OrderStatus.ALLOCATED
    assert len(stored.items) == 2
    assert all(item.server.state == ServerState.ALLOCATED for item in stored.items)


def test_allocate_insufficient_capacity_rolls_back(db_session):
    _setup_inventory()

    order_payload = {"datacenter": "VLADIMIR", "cpu_cores": 512, "ram_gb": 2048, "nvme_tb": 20.0}
    order = create_order(order_payload)

    with pytest.raises(ConflictError):
        allocate_order(order["id"])

    stored = db.session.get(Order, order["id"])
    assert stored.status == OrderStatus.NEW
    assert db.session.execute(db.select(OrderItem)).scalars().all() == []
    servers = db.session.execute(db.select(Server)).scalars().all()
    assert all(server.state == ServerState.AVAILABLE for server in servers)


def test_provision_run_once_moves_to_active(db_session, monkeypatch):
    _setup_inventory()

    order_payload = {"datacenter": "VLADIMIR", "cpu_cores": 128, "ram_gb": 512, "nvme_tb": 6.0}
    order = create_order(order_payload)
    allocate_order(order["id"])

    provision = provision_order(order["id"])
    assert provision["status"] == OrderStatus.PROVISIONING.value

    monkeypatch.setattr("mini_haas.services.provision.random.random", lambda: 0.0)
    while True:
        result = run_once()
        if result["status"] == "no_jobs":
            break

    stored = db.session.get(Order, order["id"])
    assert stored.status == OrderStatus.ACTIVE
    servers = db.session.execute(db.select(Server)).scalars().all()
    assert all(server.state == ServerState.IN_SERVICE for server in servers)
    jobs = db.session.execute(db.select(ProvisionJob)).scalars().all()
    assert all(job.status == ProvisionStatus.SUCCESS for job in jobs)


def test_provision_guard_status(db_session):
    _setup_inventory()

    order_payload = {"datacenter": "VLADIMIR", "cpu_cores": 64, "ram_gb": 256, "nvme_tb": 2.0}
    order = create_order(order_payload)

    with pytest.raises(ConflictError):
        provision_order(order["id"])
