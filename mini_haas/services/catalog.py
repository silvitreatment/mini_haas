from __future__ import annotations

from typing import Any
from ..extensions import db
from ..models import ServerModel
from .errors import ConflictError, ValidationError


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

def create_server_model(_payload: dict[str, Any]):
    name = (_payload.get("name") or "").strip()
    if not name:
        raise ValidationError("Invalid payload")

    cpu = _parse_positive_int(_payload.get("cpu_cores"))
    ram = _parse_positive_int(_payload.get("ram_gb"))
    nvme = _parse_positive_number(_payload.get("nvme_tb"))

    if cpu is None or ram is None or nvme is None:
        raise ValidationError("Invalid payload")

    existing = db.session.execute(
        db.select(ServerModel).where(ServerModel.name == name)
    ).scalar_one_or_none()

    if existing:
        raise ConflictError("Server model already exists")

    model = ServerModel(
        name=name,
        cpu_cores=cpu,
        ram_gb=ram,
        nvme_tb=nvme,
    )
    db.session.add(model)
    db.session.commit()

    return {
        "id": model.id,
        "name": model.name,
        "cpu_cores": model.cpu_cores,
        "ram_gb": model.ram_gb,
        "nvme_tb": float(model.nvme_tb),
    }
