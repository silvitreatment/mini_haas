"""Inventory service."""
from sqlalchemy import select 
from sqlalchemy import Session 

from __future__ import annotations

from typing import Any


def create_server(_payload: dict[str, Any]):
    """Create a server by barcode/datacenter/model."""
    raise NotImplementedError


def list_servers(_query: dict[str, Any]):
    """List servers by datacenter/state filters."""
    raise NotImplementedError
