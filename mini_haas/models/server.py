"""Server instance model."""

from ..extensions import db
from .enums import FirmwareDevice, ServerState
from .mixins import IdMixin, TimestampMixin


class Server(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "server"
    __table_args__ = (
        db.UniqueConstraint("barcode", name="uq_server_barcode"),
        db.UniqueConstraint("rack_id", "rack_u_position", name="uq_server_rack_u"),
        db.Index("ix_server_state_dc", "state", "datacenter_id"),
    )

    barcode = db.Column(db.String(64), nullable=False)

    model_id = db.Column(db.Integer, db.ForeignKey("server_model.id"), nullable=False)

    datacenter_id = db.Column(db.Integer, db.ForeignKey("datacenter.id"), nullable=True)
    rack_id = db.Column(db.Integer, db.ForeignKey("rack.id"), nullable=True)
    rack_u_position = db.Column(db.Integer, nullable=True)

    state = db.Column(
        db.Enum(ServerState, name="server_state"),
        nullable=False,
        server_default=ServerState.NEW.value,
    )

    allocated_to_order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)

    current_firmware_profile_id = db.Column(
        db.Integer, db.ForeignKey("firmware_profile.id"), nullable=True
    )
    current_os_image_id = db.Column(db.Integer, db.ForeignKey("os_image.id"), nullable=True)

    model = db.relationship("ServerModel", back_populates="servers")
    datacenter = db.relationship("Datacenter", back_populates="servers")
    rack = db.relationship("Rack", back_populates="servers")

    allocated_order = db.relationship("Order", back_populates="servers")
    firmware_profile = db.relationship("FirmwareProfile", back_populates="servers")
    os_image = db.relationship("OsImage", back_populates="servers")

    firmware_versions = db.relationship("ServerFirmware", back_populates="server", lazy=True)
    network_config = db.relationship("NetworkConfig", back_populates="server", uselist=False)
    telemetry_events = db.relationship("TelemetryEvent", back_populates="server", lazy=True)
    tickets = db.relationship("Ticket", back_populates="server", lazy=True)
    provision_jobs = db.relationship("ProvisionJob", back_populates="server", lazy=True)


class ServerFirmware(IdMixin, TimestampMixin, db.Model):
    __tablename__ = "server_firmware"
    __table_args__ = (
        db.UniqueConstraint("server_id", "device", name="uq_server_firmware_device"),
    )

    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)
    device = db.Column(db.Enum(FirmwareDevice, name="firmware_device"), nullable=False)
    firmware_id = db.Column(db.Integer, db.ForeignKey("firmware.id"), nullable=False)

    server = db.relationship("Server", back_populates="firmware_versions")
    firmware = db.relationship("Firmware", back_populates="server_firmwares")
