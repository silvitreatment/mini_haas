# Mini-HaaS MVP Architecture

## Goal
Minimal service that demonstrates:
- inventory of servers per datacenter
- orders for CPU/RAM/NVMe capacity
- atomic allocation with row locks
- provisioning workflow with jobs

## Layers
1) API (Flask blueprints)
   - parses input, calls services
2) Services (business rules)
   - selection, allocation, provisioning
3) Data (SQLAlchemy models)
   - schema, constraints, indexes

## Core flow
1) Add server models and servers
2) Create order
3) Allocate (transaction, SELECT FOR UPDATE)
4) Provision (create jobs, move servers to IN_SERVICE)

## State machines
- Server: AVAILABLE -> ALLOCATED -> PROVISIONING -> IN_SERVICE (or BROKEN)
- Order: NEW -> ALLOCATED -> PROVISIONING -> ACTIVE (or FAILED)
- ProvisionJob: PENDING -> RUNNING -> SUCCESS/FAILED

## Key invariants
- Server state in ALLOCATED/PROVISIONING/IN_SERVICE => allocated_order_id is not null
- AVAILABLE => allocated_order_id is null
- Allocation is all-or-nothing (no partial fulfillment)

## Minimal endpoints
- POST /server-models
- POST /servers
- GET /servers
- POST /orders
- POST /orders/{id}/allocate
- POST /orders/{id}/provision
- GET /orders/{id}
- POST /provision/run-once
