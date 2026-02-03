"""Mock auth helpers based on X-User / X-Role headers."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import request


def get_actor() -> dict[str, str | None]:
    return {
        "user": request.headers.get("X-User"),
        "role": request.headers.get("X-Role"),
    }


def require_role(role: str) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.headers.get("X-Role") != role:
                return {"error": "forbidden"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
