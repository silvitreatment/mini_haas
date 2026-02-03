"""Provisioning jobs."""

from ..extensions import db
from .enums import ProvisionStatus, ProvisionStep
from .mixins import IdMixin, TimestampMixin


class ProvisionJob(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "provision_job"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    status = db.Column(
        db.Enum(ProvisionStatus, name="provision_status"),
        nullable=False,
        server_default=ProvisionStatus.PENDING.value,
    )
    current_step = db.Column(db.Enum(ProvisionStep, name="provision_step"), nullable=True)

    attempt = db.Column(db.Integer, nullable=False, server_default="0")
    last_error = db.Column(db.Text, nullable=True)

    order = db.relationship("Order", back_populates="provision_jobs")
    server = db.relationship("Server", back_populates="provision_jobs")
