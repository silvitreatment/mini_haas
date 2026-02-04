"""Order and allocation items."""

from ..extensions import db
from .enums import OrderStatus
from .mixins import IdMixin, TimestampMixin


class Order(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "orders"

    datacenter_id = db.Column(db.Integer, db.ForeignKey("datacenter.id"), nullable=False)

    requested_cpu_cores = db.Column(db.Integer, nullable=False)
    requested_ram_gb = db.Column(db.Integer, nullable=False)
    requested_nvme_tb = db.Column(db.Numeric(6, 2), nullable=False)

    status = db.Column(
        db.Enum(OrderStatus, name="order_status"),
        nullable=False,
        server_default=OrderStatus.NEW.value,
    )

    datacenter = db.relationship("Datacenter", back_populates="orders")
    servers = db.relationship("Server", back_populates="allocated_order", lazy=True)
    items = db.relationship("OrderItem", back_populates="order", lazy=True)
    provision_jobs = db.relationship("ProvisionJob", back_populates="order", lazy=True)


class OrderItem(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "order_item"
    __table_args__ = (
        db.UniqueConstraint("server_id", name="uq_order_item_server"),
    )

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    order = db.relationship("Order", back_populates="items")
    server = db.relationship("Server", back_populates="order_items")
