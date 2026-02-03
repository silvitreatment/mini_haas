"""Transactional allocation service."""

from __future__ import annotations

from typing import Any


def allocate_order(*_args: Any, **_kwargs: Any):
    """Reserve servers for order using SELECT FOR UPDATE.

    Must raise a conflict error if capacity changed.
    """
    raise NotImplementedError
