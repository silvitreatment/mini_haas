"""Model registry import."""

from .allocation import AllocationPlan, AllocationPlanItem
from .audit import AuditLog
from .component import ComponentModel, WarehouseStock
from .datacenter import Datacenter
from .firmware import Firmware, FirmwareProfile, FirmwareProfileItem, FirmwareUpgradePath
from .network import NetworkConfig
from .order import Order
from .os_image import OsImage, OsImageCompat
from .provision import ProvisionJob
from .rack import Rack
from .server import Server, ServerFirmware
from .server_model import ServerModel
from .telemetry import TelemetryEvent
from .ticket import Ticket
from .warehouse import Warehouse

__all__ = [
    "AllocationPlan",
    "AllocationPlanItem",
    "AuditLog",
    "ComponentModel",
    "Datacenter",
    "Firmware",
    "FirmwareProfile",
    "FirmwareProfileItem",
    "FirmwareUpgradePath",
    "NetworkConfig",
    "Order",
    "OsImage",
    "OsImageCompat",
    "ProvisionJob",
    "Rack",
    "Server",
    "ServerFirmware",
    "ServerModel",
    "TelemetryEvent",
    "Ticket",
    "Warehouse",
    "WarehouseStock",
]
