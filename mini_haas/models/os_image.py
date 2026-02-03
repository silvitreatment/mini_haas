"""OS image catalog and compatibility."""

from ..extensions import db
from .mixins import IdMixin, TimestampMixin


class OsImage(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "os_image"
    __table_args__ = (
        db.UniqueConstraint("name", "version", name="uq_os_image"),
    )

    name = db.Column(db.String(128), nullable=False)
    version = db.Column(db.String(64), nullable=False)
    checksum = db.Column(db.String(128), nullable=True)

    compat = db.relationship("OsImageCompat", back_populates="os_image", lazy=True)
    servers = db.relationship("Server", back_populates="os_image", lazy=True)


class OsImageCompat(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "os_image_compat"
    __table_args__ = (
        db.UniqueConstraint("os_image_id", "server_model_id", name="uq_os_image_compat"),
    )

    os_image_id = db.Column(db.Integer, db.ForeignKey("os_image.id"), nullable=False)
    server_model_id = db.Column(db.Integer, db.ForeignKey("server_model.id"), nullable=False)

    os_image = db.relationship("OsImage", back_populates="compat")
    server_model = db.relationship("ServerModel", back_populates="os_image_compat")
