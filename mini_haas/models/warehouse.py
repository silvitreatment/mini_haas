"""Warehouse model."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class Warehouse(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "warehouse"
    __table_args__ = (
        db.UniqueConstraint("datacenter_id", "name", name="uq_warehouse_dc_name"),
    )

    datacenter_id = db.Column(db.Integer, db.ForeignKey("datacenter.id"), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    datacenter = db.relationship("Datacenter", back_populates="warehouses")
    stock = db.relationship("WarehouseStock", back_populates="warehouse", lazy=True)
