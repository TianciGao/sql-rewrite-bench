# LLM-R2 Common-core PG Expansion Approval Gate v1

- `approval_status = not_approved`
- `approved_for_pg_generation = no`
- `approved_for_pg_execution = no`
- `approved_for_checker = no`
- `approved_for_timing = no`
- `approved_for_speedup = no`
- `approved_for_mysql_spark = no`
- `approved_for_pg40 = no`
- `approved_for_full120 = no`
- `approved_for_result_card = no`

## Required Human Confirmations Before Any Run

- candidate slice accepted
- runner support basis accepted
- source/DDL/witness paths accepted
- no timing planned
- no MySQL/Spark planned
- failure bucket policy accepted
- prior PG3 evidence kept separate from expansion slice

## Boundary

This gate does not authorize expansion automatically.
It does not authorize PostgreSQL generation, execution, checker, timing, or
speedup.
