"""Datacenter model."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class Datacenter(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "datacenter"

    name = db.Column(db.String(64), unique=True, nullable=False)

    servers = db.relationship("Server", back_populates="datacenter", lazy=True)
    orders = db.relationship("Order", back_populates="datacenter", lazy=True)
