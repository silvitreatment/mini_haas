"""Seed demo data for local development."""

from ..app import create_app
from ..extensions import db


def main() -> None:
    app = create_app()
    with app.app_context():
        # TODO: implement demo seed logic
        db.session.commit()


if __name__ == "__main__":
    main()
