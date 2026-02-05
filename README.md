# mini_haas (MVP)

Mini‑HaaS: инвентарь → заказ → атомарное резервирование → provisioning.

## Структура
- `mini_haas/app.py` - create_app
- `mini_haas/models/` - таблицы 
- `mini_haas/services/` - бизнес-правила
- `mini_haas/api/` - REST эндпоинты
- `docs/architecture.md` - архитектура

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

## Demo сценарий (curl)
```bash
curl -X POST localhost:5000/datacenters -H "Content-Type: application/json" \
  -d '{"name":"VLADIMIR"}'

curl -X POST localhost:5000/server-models -H "Content-Type: application/json" \
  -d '{"name":"Dell-R740-64c-512g-4tb","cpu_cores":64,"ram_gb":512,"nvme_tb":4.0}'

curl -X POST localhost:5000/servers -H "Content-Type: application/json" \
  -d '{"barcode":"SRV-0001","datacenter":"VLADIMIR","model_name":"Dell-R740-64c-512g-4tb"}'

curl -X POST localhost:5000/servers -H "Content-Type: application/json" \
  -d '{"barcode":"SRV-0002","datacenter":"VLADIMIR","model_name":"Dell-R740-64c-512g-4tb"}'

curl -X POST localhost:5000/orders -H "Content-Type: application/json" \
  -d '{"datacenter":"VLADIMIR","cpu_cores":128,"ram_gb":512,"nvme_tb":6.0}'

curl -X POST localhost:5000/orders/1/allocate

curl -X POST localhost:5000/orders/1/provision

curl -X POST localhost:5000/provision/run-once

curl -X GET localhost:5000/orders/1
```

## Тесты
```bash
TEST_DATABASE_URL=postgresql+psycopg://mini_haas:mini_haas@localhost:5432/mini_haas pytest
```
