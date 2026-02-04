# mini_haas (MVP)

Минимальная архитектура для Mini‑HaaS: инвентарь → заказ → атомарное резервирование → provisioning.

## Структура
- `mini_haas/app.py` — create_app
- `mini_haas/models/` — таблицы MVP
- `mini_haas/services/` — бизнес‑правила
- `mini_haas/api/` — REST эндпоинты
- `docs/architecture.md` — архитектура

## Быстрый старт
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
