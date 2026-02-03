"""Network configuration per server."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class NetworkConfig(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "network_config"
    __table_args__ = (
        db.UniqueConstraint("server_id", name="uq_network_server"),
    )

    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)
    ip = db.Column(db.String(64), nullable=False)
    vlan = db.Column(db.String(64), nullable=True)
    hostname = db.Column(db.String(128), nullable=True)

    server = db.relationship("Server", back_populates="network_config")
