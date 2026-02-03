"""Telemetry events."""

from ..extensions import db
from .enums import TelemetryType
from .mixins import IdMixin, TimestampMixin


class TelemetryEvent(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "telemetry_event"
    __table_args__ = (
        db.Index("ix_telemetry_server_ts", "server_id", "ts"),
        db.UniqueConstraint("event_hash", name="uq_telemetry_event_hash"),
    )

    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)
    ts = db.Column(db.DateTime(timezone=True), nullable=False)
    type = db.Column(db.Enum(TelemetryType, name="telemetry_type"), nullable=False)
    payload = db.Column(db.JSON, nullable=True)

    event_hash = db.Column(db.String(128), nullable=True)

    server = db.relationship("Server", back_populates="telemetry_events")
