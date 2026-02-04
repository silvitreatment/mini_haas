# MVP test cases

- Allocate covers order and creates order_items
- Allocate rollback on insufficient capacity (no server state changes)
- Two concurrent allocate calls: one success, one 409
- Provision moves servers to IN_SERVICE and order to ACTIVE
