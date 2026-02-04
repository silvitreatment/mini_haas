"""Provisioning jobs."""

from ..extensions import db
from .enums import ProvisionStatus
from .mixins import IdMixin, TimestampMixin


class ProvisionJob(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "provision_job"
    __table_args__ = (
        db.UniqueConstraint("server_id", name="uq_provision_job_server"),
    )

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    status = db.Column(
        db.Enum(ProvisionStatus, name="provision_status"),
        nullable=False,
        server_default=ProvisionStatus.PENDING.value,
    )
    attempt = db.Column(db.Integer, nullable=False, server_default="0")
    last_error = db.Column(db.Text, nullable=True)

    order = db.relationship("Order", back_populates="provision_jobs")
    server = db.relationship("Server", back_populates="provision_jobs")
