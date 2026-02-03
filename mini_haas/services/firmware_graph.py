"""Firmware upgrade path resolution."""

from __future__ import annotations

from typing import Any, Iterable


def find_upgrade_path(*_args: Any, **_kwargs: Any) -> Iterable[Any]:
    """Return a firmware upgrade chain using BFS over FirmwareUpgradePath."""
    raise NotImplementedError
