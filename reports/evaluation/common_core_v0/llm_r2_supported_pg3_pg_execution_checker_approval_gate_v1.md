# LLM-R2 Supported PG3 PostgreSQL Execution/Checker Approval Gate v1

- `approval_status = not_approved`
- `approved_for_pg_execution = no`
- `approved_for_checker = no`
- `approved_for_timing = no`
- `approved_for_speedup = no`
- `approved_for_mysql_spark = no`
- `approved_for_full_120 = no`
- `approved_for_result_card = no`

## Required Human Confirmations Before Approval

- generated SQL paths accepted
- source SQL paths recovered
- DDL/witness paths recovered
- workspace layout accepted
- no timing planned
- no result card planned
- failure bucket policy accepted

## Boundary

This approval gate does not authorize execution.
This approval gate does not authorize checker.
This approval gate does not authorize timing or speedup.
This approval gate does not create correctness or exact-match evidence.
