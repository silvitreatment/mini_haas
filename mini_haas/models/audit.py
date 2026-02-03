"""Audit log entries."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class AuditLog(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "audit_log"

    actor = db.Column(db.String(128), nullable=True)
    action = db.Column(db.String(128), nullable=False)

    entity_type = db.Column(db.String(64), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)

    from_state = db.Column(db.String(64), nullable=True)
    to_state = db.Column(db.String(64), nullable=True)
