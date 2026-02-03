# Minimal test cases

- TC-1 Scan to rack: place server in RACK-1 U10, second to same U -> 409
- TC-2 Planning: order requires 100 cores, servers 64 + 32 -> plan picks both or returns insufficient
- TC-3 Allocate race: two orders allocate same server -> one success, second 409
- TC-4 Firmware chain: 1.0 -> 1.1 -> 1.2 exists -> SUCCESS
- TC-5 No firmware path: 1.0 -> 2.0 missing -> FAILED
- TC-6 Telemetry ticket: SMART_FAIL -> REPLACE_DISK with stock -> ticket has warehouse_id and component
- TC-7 Ticket dedup: two SMART_FAIL -> one OPEN ticket
