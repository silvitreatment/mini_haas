"""Server model (factory configuration)."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class ServerModel(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "server_model"

    name = db.Column(db.String(128), unique=True, nullable=False)
    cpu_cores = db.Column(db.Integer, nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    nvme_tb = db.Column(db.Numeric(6, 2), nullable=False)

    servers = db.relationship("Server", back_populates="model", lazy=True)
