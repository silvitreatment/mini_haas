"""Provision runner service."""

from __future__ import annotations

from typing import Any


def run_once() -> dict[str, Any]:
    """Pick one PENDING job and mark SUCCESS/FAILED."""
    raise NotImplementedError
