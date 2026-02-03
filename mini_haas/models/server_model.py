"""Server model (factory configuration)."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class ServerModel(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "server_model"
    __table_args__ = (
        db.UniqueConstraint("vendor", "model", name="uq_server_model_vendor_model"),
    )

    vendor = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)

    cpu_cores = db.Column(db.Integer, nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    nvme_tb = db.Column(db.Numeric(10, 2), nullable=False)
    gpu_count = db.Column(db.Integer, nullable=True)

    power_kw = db.Column(db.Numeric(10, 2), nullable=True)
    cooling_kw = db.Column(db.Numeric(10, 2), nullable=True)
    weight_kg = db.Column(db.Numeric(10, 2), nullable=True)

    servers = db.relationship("Server", back_populates="model", lazy=True)
    firmwares = db.relationship("Firmware", back_populates="server_model", lazy=True)
    os_image_compat = db.relationship("OsImageCompat", back_populates="server_model", lazy=True)
