"""Maintenance tickets."""

from ..extensions import db
from .enums import TicketPriority, TicketStatus, TicketType
from .mixins import IdMixin, TimestampMixin


class Ticket(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "ticket"
    __table_args__ = (
        db.Index("ix_ticket_status_created", "status", "created_at"),
    )

    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    type = db.Column(db.Enum(TicketType, name="ticket_type"), nullable=False)
    priority = db.Column(db.Enum(TicketPriority, name="ticket_priority"), nullable=False)
    status = db.Column(
        db.Enum(TicketStatus, name="ticket_status"),
        nullable=False,
        server_default=TicketStatus.OPEN.value,
    )

    instructions = db.Column(db.Text, nullable=True)

    recommended_spare_component_model_id = db.Column(
        db.Integer, db.ForeignKey("component_model.id"), nullable=True
    )
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"), nullable=True)

    server = db.relationship("Server", back_populates="tickets")
    recommended_component = db.relationship("ComponentModel")
    warehouse = db.relationship("Warehouse")
