"""Server instance."""

from ..extensions import db
from .enums import ServerState
from .mixins import IdMixin, TimestampMixin


class Server(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "server"
    __table_args__ = (
        db.UniqueConstraint("barcode", name="uq_server_barcode"),
        db.Index("ix_server_state_dc", "state", "datacenter_id"),
    )

    barcode = db.Column(db.String(64), nullable=False)

    datacenter_id = db.Column(db.Integer, db.ForeignKey("datacenter.id"), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("server_model.id"), nullable=False)

    state = db.Column(
        db.Enum(ServerState, name="server_state"),
        nullable=False,
        server_default=ServerState.AVAILABLE.value,
    )

    allocated_order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)

    datacenter = db.relationship("Datacenter", back_populates="servers")
    model = db.relationship("ServerModel", back_populates="servers")
    allocated_order = db.relationship("Order", back_populates="servers")
    order_items = db.relationship("OrderItem", back_populates="server", lazy=True)
    provision_jobs = db.relationship("ProvisionJob", back_populates="server", lazy=True)
