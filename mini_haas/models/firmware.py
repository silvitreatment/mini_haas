"""Firmware models and upgrade graph."""

from ..extensions import db
from .enums import FirmwareDevice
from .mixins import IdMixin, TimestampMixin


class Firmware(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "firmware"
    __table_args__ = (
        db.UniqueConstraint("device", "version", "server_model_id", name="uq_firmware"),
    )

    device = db.Column(db.Enum(FirmwareDevice, name="firmware_device"), nullable=False)
    version = db.Column(db.String(64), nullable=False)

    server_model_id = db.Column(db.Integer, db.ForeignKey("server_model.id"), nullable=True)

    server_model = db.relationship("ServerModel", back_populates="firmwares")
    from_paths = db.relationship(
        "FirmwareUpgradePath",
        back_populates="from_firmware",
        foreign_keys="FirmwareUpgradePath.from_firmware_id",
    )
    to_paths = db.relationship(
        "FirmwareUpgradePath",
        back_populates="to_firmware",
        foreign_keys="FirmwareUpgradePath.to_firmware_id",
    )
    profile_items = db.relationship("FirmwareProfileItem", back_populates="firmware")
    server_firmwares = db.relationship("ServerFirmware", back_populates="firmware")


class FirmwareUpgradePath(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "firmware_upgrade_path"
    __table_args__ = (
        db.UniqueConstraint("from_firmware_id", "to_firmware_id", name="uq_firmware_path"),
    )

    from_firmware_id = db.Column(db.Integer, db.ForeignKey("firmware.id"), nullable=False)
    to_firmware_id = db.Column(db.Integer, db.ForeignKey("firmware.id"), nullable=False)

    from_firmware = db.relationship(
        "Firmware", foreign_keys=[from_firmware_id], back_populates="from_paths"
    )
    to_firmware = db.relationship(
        "Firmware", foreign_keys=[to_firmware_id], back_populates="to_paths"
    )


class FirmwareProfile(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "firmware_profile"

    name = db.Column(db.String(128), unique=True, nullable=False)

    items = db.relationship("FirmwareProfileItem", back_populates="profile", lazy=True)
    servers = db.relationship("Server", back_populates="firmware_profile", lazy=True)


class FirmwareProfileItem(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "firmware_profile_item"
    __table_args__ = (
        db.UniqueConstraint("profile_id", "device", name="uq_profile_device"),
    )

    profile_id = db.Column(db.Integer, db.ForeignKey("firmware_profile.id"), nullable=False)
    device = db.Column(db.Enum(FirmwareDevice, name="firmware_device"), nullable=False)
    firmware_id = db.Column(db.Integer, db.ForeignKey("firmware.id"), nullable=False)

    profile = db.relationship("FirmwareProfile", back_populates="items")
    firmware = db.relationship("Firmware", back_populates="profile_items")
