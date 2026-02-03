"""Component catalog and warehouse stock."""

from ..extensions import db
from .enums import ComponentType
from .mixins import IdMixin, TimestampMixin


class ComponentModel(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "component_model"
    __table_args__ = (
        db.UniqueConstraint("type", "vendor", "model", name="uq_component_model"),
    )

    type = db.Column(db.Enum(ComponentType, name="component_type"), nullable=False)
    vendor = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)

    capacity_gb = db.Column(db.Integer, nullable=True)
    capacity_tb = db.Column(db.Numeric(10, 2), nullable=True)

    stock = db.relationship("WarehouseStock", back_populates="component_model", lazy=True)


class WarehouseStock(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "warehouse_stock"
    __table_args__ = (
        db.UniqueConstraint("warehouse_id", "component_model_id", name="uq_stock_item"),
    )

    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"), nullable=False)
    component_model_id = db.Column(
        db.Integer, db.ForeignKey("component_model.id"), nullable=False
    )
    qty_available = db.Column(db.Integer, nullable=False, server_default="0")

    warehouse = db.relationship("Warehouse", back_populates="stock")
    component_model = db.relationship("ComponentModel", back_populates="stock")
