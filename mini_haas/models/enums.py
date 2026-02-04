"""Domain enums for MVP."""

from enum import Enum


class ServerState(str, Enum):
    AVAILABLE = "AVAILABLE"
    ALLOCATED = "ALLOCATED"
    PROVISIONING = "PROVISIONING"
    IN_SERVICE = "IN_SERVICE"
    BROKEN = "BROKEN"


class OrderStatus(str, Enum):
    NEW = "NEW"
    ALLOCATED = "ALLOCATED"
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


class ProvisionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
