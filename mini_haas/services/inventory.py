"""Inventory service: scan and placement rules."""

from __future__ import annotations

from typing import Any


def scan_server(*_args: Any, **_kwargs: Any):
    """Create or update a server based on scan payload.

    Responsibilities:
    - Create server if barcode not found
    - Enforce rack position uniqueness
    - Move server between warehouse and rack
    """
    raise NotImplementedError


def list_servers(*_args: Any, **_kwargs: Any):
    """List servers with filters (state, datacenter, rack)."""
    raise NotImplementedError


def get_server(*_args: Any, **_kwargs: Any):
    """Return server details by id."""
    raise NotImplementedError
