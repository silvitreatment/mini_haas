"""Allocation plan models."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class AllocationPlan(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "allocation_plan"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True, nullable=False)
    algorithm_version = db.Column(db.String(64), nullable=False)

    order = db.relationship("Order", back_populates="allocation_plan")
    items = db.relationship("AllocationPlanItem", back_populates="plan", lazy=True)


class AllocationPlanItem(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "allocation_plan_item"
    __table_args__ = (
        db.UniqueConstraint("plan_id", "server_id", name="uq_plan_server"),
    )

    plan_id = db.Column(db.Integer, db.ForeignKey("allocation_plan.id"), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    cpu_cores = db.Column(db.Integer, nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    nvme_tb = db.Column(db.Numeric(10, 2), nullable=False)

    plan = db.relationship("AllocationPlan", back_populates="items")
    server = db.relationship("Server")
