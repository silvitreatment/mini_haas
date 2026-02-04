from __future__ import annotations

from typing import Any

from sqlalchemy import select

from ..extensions import db
from ..models import Datacenter, Server, ServerModel
from ..models.enums import ServerState
from .errors import ConflictError, NotFoundError, ValidationError


def create_server(_payload: dict[str, Any]):
    barcode = (_payload.get("barcode") or "").strip()
    datacenter_name = (_payload.get("datacenter") or "").strip()
    model_name = (_payload.get("model_name") or "").strip()

    if not barcode or not datacenter_name or not model_name:
        raise ValidationError("Invalid payload")

    datacenter = db.session.execute(
        select(Datacenter).where(Datacenter.name == datacenter_name)
    ).scalar_one_or_none()
    if not datacenter:
        raise NotFoundError("datacenter not found")

    model = db.session.execute(
        select(ServerModel).where(ServerModel.name == model_name)
    ).scalar_one_or_none()
    if not model:
        raise NotFoundError("server model not found")

    existing = db.session.execute(
        select(Server).where(Server.barcode == barcode)
    ).scalar_one_or_none()
    if existing:
        raise ConflictError("server already exists")

    server = Server(
        barcode=barcode,
        datacenter_id=datacenter.id,
        model_id=model.id,
    )
    db.session.add(server)
    db.session.commit()

    return {
        "id": server.id,
        "barcode": server.barcode,
        "datacenter": datacenter.name,
        "model": model.name,
        "state": server.state.value,
    }


def list_servers(_query: dict[str, Any]):
    dc = (_query.get("dc") or "").strip()
    state_value = (_query.get("state") or "").strip().upper()

    stmt = select(Server).join(Server.datacenter).join(Server.model)

    if dc:
        stmt = stmt.where(Datacenter.name == dc)

    if state_value:
        try:
            state = ServerState(state_value)
        except ValueError as exc:
            raise ValidationError("Invalid state") from exc
        stmt = stmt.where(Server.state == state)

    servers = db.session.execute(stmt).scalars().all()
    return [
        {
            "id": server.id,
            "barcode": server.barcode,
            "datacenter": server.datacenter.name,
            "model": server.model.name,
            "state": server.state.value,
        }
        for server in servers
    ]
