"""Provisioning service and worker hooks."""

from __future__ import annotations

from typing import Any


def create_jobs_for_order(*_args: Any, **_kwargs: Any):
    """Create ProvisionJob records for each allocated server."""
    raise NotImplementedError


def run_next_job(*_args: Any, **_kwargs: Any):
    """Worker entry point: pick PENDING job and execute steps."""
    raise NotImplementedError
