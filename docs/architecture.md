# Architecture - Mini-HaaS

## Goals
- Track inventory across datacenters, racks, and warehouses
- Plan and allocate capacity transactionally
- Run provisioning workflows with firmware upgrade paths
- Ingest telemetry and auto-generate tickets with spare part selection

## Layered design
1) API (Flask blueprints)
   - Thin HTTP handlers, parse/validate payloads, call services
2) Services (business rules)
   - Planning, allocation, provisioning, telemetry/ticketing, inventory
3) Data (SQLAlchemy models)
   - Enforces schema, indexes, and constraints
4) Worker
   - Polling loop for provisioning jobs

## Project layout
```
mini_haas/
  app.py                # create_app
  config.py             # env-driven config
  extensions.py         # db + migrations
  api/                  # Flask blueprints
  models/               # SQLAlchemy models
  services/             # business rules
  workers/              # provisioning worker loop
  schemas/              # request validators (placeholder)
  scripts/              # seed/demo utilities
migrations/             # Alembic migrations
Docs:
  docs/architecture.md
  tests/test_cases.md
```

## Core workflows
### Inventory scan
- Input: barcode + location (warehouse or rack)
- If server missing: create with state IN_WAREHOUSE (or NEW -> IN_WAREHOUSE)
- If rack placement: enforce unique (rack_id, rack_u_position)
- Update datacenter/rack linkage and timestamps

### Planning
- Input: Order with requested cpu/ram/nvme and datacenter
- Eligible states: IN_WAREHOUSE or RACKED (choose one for MVP)
- Exclude: BROKEN, REPAIRING, ALLOCATED, PROVISIONING, IN_SERVICE, DECOMMISSIONED
- Greedy selection by model cpu_cores desc (or composite score)
- Output: AllocationPlan + AllocationPlanItem rows, Order -> PLANNED

### Allocation (transactional)
- Input: AllocationPlan for order
- Transaction:
  - SELECT ... FOR UPDATE servers in plan
  - If any server not in allocatable state -> 409 conflict
  - Update server.state = ALLOCATED, allocated_to_order_id = order.id
- Order -> ALLOCATED

### Provisioning
- POST /orders/{id}/provision
- Creates ProvisionJob per server, Order -> PROVISIONING
- Worker loop:
  - Pick PENDING job, set RUNNING
  - Execute steps in fixed order
  - Firmware logic: if current != target, find upgrade chain via FirmwareUpgradePath (BFS)
  - If missing path -> FAILED, with last_error
  - On success: server.state = IN_SERVICE, job SUCCESS

### Telemetry -> tickets
- POST /telemetry accepts array
- Dedup via event_hash (unique)
- Rules:
  - SMART_FAIL -> REPLACE_DISK (priority HIGH)
  - ECC_ERRORS (count > threshold) -> REPLACE_RAM
  - OVERHEAT -> CHECK_COOLING
- Ticket dedup: do not create if same type ticket already OPEN
- Suppression: if datacenter.power_outage = true, skip REBOOT tickets
- Spare part selection: WarehouseStock in same DC with qty_available > 0

## State machines
- Server: NEW -> IN_FACTORY_TEST -> IN_TRANSIT -> IN_WAREHOUSE -> RACKED -> ALLOCATED -> PROVISIONING -> IN_SERVICE
  - BROKEN -> REPAIRING -> IN_WAREHOUSE or DECOMMISSIONED
- Order: DRAFT -> PLANNED -> ALLOCATED -> PROVISIONING -> ACTIVE (or FAILED/CANCELLED)
- ProvisionJob: PENDING -> RUNNING -> SUCCESS/FAILED/CANCELLED
- Ticket: OPEN -> IN_PROGRESS -> DONE/WONT_FIX

## Data constraints and indexes
- server.barcode unique
- server(state, datacenter_id) index
- telemetry_event(server_id, ts) index
- ticket(status, created_at) index
- rack_id + rack_u_position unique
- event_hash unique for telemetry dedup

## Transaction boundaries
- Allocation is the only multi-row transactional write with row locks
- Worker updates are per-job within a transaction
- Telemetry ingestion uses upsert semantics on event_hash

## Operational notes
- Auth is mocked via X-User / X-Role headers
- Use Alembic for migrations
- Logs: optional AuditLog rows on state transitions
