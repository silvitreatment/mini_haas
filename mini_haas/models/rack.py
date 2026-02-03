"""Rack model."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class Rack(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "rack"
    __table_args__ = (
        db.UniqueConstraint("datacenter_id", "name", name="uq_rack_dc_name"),
    )

    datacenter_id = db.Column(db.Integer, db.ForeignKey("datacenter.id"), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    u_capacity = db.Column(db.Integer, nullable=False, server_default="42")
    power_kw_limit = db.Column(db.Numeric(10, 2), nullable=True)
    cooling_kw_limit = db.Column(db.Numeric(10, 2), nullable=True)

    datacenter = db.relationship("Datacenter", back_populates="racks")
    servers = db.relationship("Server", back_populates="rack", lazy=True)
