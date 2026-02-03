"""Order planning service (allocation plan builder)."""

from __future__ import annotations

from typing import Any


def build_allocation_plan(*_args: Any, **_kwargs: Any):
    """Create AllocationPlan using greedy model ordering.

    Should:
    - Select servers in IN_WAREHOUSE or RACKED state
    - Exclude non-allocatable states
    - Sort by power (cpu_cores desc) or composite score
    - Record plan items with resource coverage
    """
    raise NotImplementedError
