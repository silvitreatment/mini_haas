"""Domain enums."""

from enum import Enum


class ServerState(str, Enum):
    NEW = "NEW"
    IN_FACTORY_TEST = "IN_FACTORY_TEST"
    IN_TRANSIT = "IN_TRANSIT"
    IN_WAREHOUSE = "IN_WAREHOUSE"
    RACKED = "RACKED"
    ALLOCATED = "ALLOCATED"
    PROVISIONING = "PROVISIONING"
    IN_SERVICE = "IN_SERVICE"
    BROKEN = "BROKEN"
    REPAIRING = "REPAIRING"
    DECOMMISSIONED = "DECOMMISSIONED"


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    ALLOCATED = "ALLOCATED"
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ProvisionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ProvisionStep(str, Enum):
    FLASH_BIOS = "FLASH_BIOS"
    FLASH_BMC = "FLASH_BMC"
    INSTALL_OS = "INSTALL_OS"
    CONFIG_NETWORK = "CONFIG_NETWORK"
    POWER_CYCLE = "POWER_CYCLE"
    FINAL_HEALTHCHECK = "FINAL_HEALTHCHECK"


class TelemetryType(str, Enum):
    SMART_FAIL = "SMART_FAIL"
    ECC_ERRORS = "ECC_ERRORS"
    OVERHEAT = "OVERHEAT"


class TicketType(str, Enum):
    REBOOT = "REBOOT"
    REPLACE_DISK = "REPLACE_DISK"
    REPLACE_RAM = "REPLACE_RAM"
    CHECK_COOLING = "CHECK_COOLING"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    WONT_FIX = "WONT_FIX"


class ComponentType(str, Enum):
    DISK = "DISK"
    RAM = "RAM"
    PSU = "PSU"


class FirmwareDevice(str, Enum):
    BIOS = "BIOS"
    BMC = "BMC"
    NVME = "NVME"
