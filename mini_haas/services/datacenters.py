"""Datacenter service."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select

from ..extensions import db
from ..models import Datacenter
from .errors import ConflictError, ValidationError


def create_datacenter(_payload: dict[str, Any]):
    name = (_payload.get("name") or "").strip()
    if not name:
        raise ValidationError("Invalid payload")

    existing = db.session.execute(
        select(Datacenter).where(Datacenter.name == name)
    ).scalar_one_or_none()
    if existing:
        raise ConflictError("datacenter already exists")

    datacenter = Datacenter(name=name)
    db.session.add(datacenter)
    db.session.commit()

    return {"id": datacenter.id, "name": datacenter.name}
