"""Model mixins."""

from sqlalchemy import func

from ..extensions import db


class IdMixin:
    id = db.Column(db.Integer, primary_key=True)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
