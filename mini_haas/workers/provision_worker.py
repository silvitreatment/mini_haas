"""Provisioning worker entry point."""

import time

from ..app import create_app
from ..extensions import db
from ..services import provisioning


def run_forever() -> None:
    app = create_app()
    with app.app_context():
        while True:
            provisioning.run_next_job(db.session)
            time.sleep(app.config["PROVISION_POLL_SECONDS"])


if __name__ == "__main__":
    run_forever()
