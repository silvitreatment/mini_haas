"""Datacenter model."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class Datacenter(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "datacenter"

    name = db.Column(db.String(64), unique=True, nullable=False)
    location = db.Column(db.String(128), nullable=True)

    max_power_kw = db.Column(db.Numeric(10, 2), nullable=True)
    max_cooling_kw = db.Column(db.Numeric(10, 2), nullable=True)

    # MVP: used to suppress or downgrade tickets during outage
    power_outage = db.Column(db.Boolean, nullable=False, server_default="false")

    racks = db.relationship("Rack", back_populates="datacenter", lazy=True)
    warehouses = db.relationship("Warehouse", back_populates="datacenter", lazy=True)
    servers = db.relationship("Server", back_populates="datacenter", lazy=True)
    orders = db.relationship("Order", back_populates="datacenter", lazy=True)
