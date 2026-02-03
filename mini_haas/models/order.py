"""Order model."""

from ..extensions import db
from .enums import OrderStatus
from .mixins import IdMixin, TimestampMixin


class Order(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "orders"

    requester = db.Column(db.String(128), nullable=True)
    datacenter_id = db.Column(db.Integer, db.ForeignKey("datacenter.id"), nullable=False)

    requested_cpu_cores = db.Column(db.Integer, nullable=False)
    requested_ram_gb = db.Column(db.Integer, nullable=False)
    requested_nvme_tb = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(
        db.Enum(OrderStatus, name="order_status"),
        nullable=False,
        server_default=OrderStatus.DRAFT.value,
    )

    datacenter = db.relationship("Datacenter", back_populates="orders")
    allocation_plan = db.relationship("AllocationPlan", back_populates="order", uselist=False)
    servers = db.relationship("Server", back_populates="allocated_order", lazy=True)
    provision_jobs = db.relationship("ProvisionJob", back_populates="order", lazy=True)
