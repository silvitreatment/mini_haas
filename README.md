# mini_haas

Mini-HaaS service skeleton (Flask + PostgreSQL + SQLAlchemy).

## Structure
- `mini_haas/` application package
- `mini_haas/api/` REST endpoints (blueprints)
- `mini_haas/models/` SQLAlchemy models
- `mini_haas/services/` business rules
- `mini_haas/workers/` provisioning worker
- `docs/architecture.md` system architecture
- `tests/test_cases.md` minimal test cases

## Quickstart (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

export FLASK_APP=mini_haas.app:create_app
export DATABASE_URL=postgresql+psycopg://mini_haas:mini_haas@localhost:5432/mini_haas

flask db init
flask db migrate -m "init"
flask db upgrade

flask run
```

Provisioning worker:
```bash
python -m mini_haas.workers.provision_worker
```

## Docs
- Architecture and workflow notes: `docs/architecture.md`
- Test cases: `tests/test_cases.md`
