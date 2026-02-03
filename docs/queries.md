# Key SQL queries

## Candidates for planning
```sql
SELECT s.*
FROM server s
JOIN server_model m ON m.id = s.model_id
WHERE s.datacenter_id = :dc_id
  AND s.state IN ('IN_WAREHOUSE', 'RACKED')
ORDER BY m.cpu_cores DESC;
```

## Allocation (transactional)
```sql
SELECT *
FROM server
WHERE id = ANY(:server_ids)
FOR UPDATE;

UPDATE server
SET state = 'ALLOCATED', allocated_to_order_id = :order_id
WHERE id = ANY(:server_ids);
```

## Firmware upgrade graph edges
```sql
SELECT from_firmware_id, to_firmware_id
FROM firmware_upgrade_path
WHERE from_firmware_id IN (:frontier);
```

## Spare part selection
```sql
SELECT ws.*
FROM warehouse_stock ws
JOIN warehouse w ON w.id = ws.warehouse_id
WHERE w.datacenter_id = :dc_id
  AND ws.qty_available > 0
  AND ws.component_model_id = :component_model_id
LIMIT 1;
```

## Provisioning progress per order
```sql
SELECT status, COUNT(*)
FROM provision_job
WHERE order_id = :order_id
GROUP BY status;
```
