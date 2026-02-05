from __future__ import annotations

import threading

import pytest

from mini_haas.extensions import db
from mini_haas.models import Datacenter, Order, Server, ServerModel
from mini_haas.models.enums import OrderStatus
from mini_haas.services.errors import ConflictError
from mini_haas.services.orders import allocate_order, create_order


def _setup_inventory():
    dc = Datacenter(name="VLADIMIR")
    model = ServerModel(name="Dell-R740-64c-512g-4tb", cpu_cores=64, ram_gb=512, nvme_tb=4.0)
    servers = [
        Server(barcode="SRV-0001", datacenter=dc, model=model),
        Server(barcode="SRV-0002", datacenter=dc, model=model),
    ]
    db.session.add_all([dc, model, *servers])
    db.session.commit()


def test_concurrent_allocate_one_wins(app, db_session):
    _setup_inventory()

    order1 = create_order({"datacenter": "VLADIMIR", "cpu_cores": 128, "ram_gb": 512, "nvme_tb": 6.0})
    order2 = create_order({"datacenter": "VLADIMIR", "cpu_cores": 128, "ram_gb": 512, "nvme_tb": 6.0})

    results = []
    barrier = threading.Barrier(2)

    def _worker(order_id: int):
        with app.app_context():
            barrier.wait()
            try:
                allocate_order(order_id)
                results.append("success")
            except ConflictError:
                results.append("conflict")
            finally:
                db.session.remove()

    t1 = threading.Thread(target=_worker, args=(order1["id"],))
    t2 = threading.Thread(target=_worker, args=(order2["id"],))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert sorted(results) == ["conflict", "success"]

    stored_orders = db.session.execute(db.select(Order)).scalars().all()
    statuses = sorted(order.status for order in stored_orders)
    assert statuses == [OrderStatus.ALLOCATED, OrderStatus.NEW]
