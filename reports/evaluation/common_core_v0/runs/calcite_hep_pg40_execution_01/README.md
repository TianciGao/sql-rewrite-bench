# Calcite HEP PG40 Execution

This package prepares human-run PostgreSQL execution and validity evidence for Calcite HEP on the frozen `common_core_v0_40_pg40` denominator.

## Scope

- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- `denominator_id = common_core_v0_40_pg40`
- planned rows: `40`
- execution targets: `29`
- preserved non-executed generation failures: `11`

## Row Policy

- execute only rows with `generation_status = generation_success`
- preserve generation failures explicitly as `not_executed_generation_failed`
- do not silently drop any denominator row

## How To Run

From repo root:

```bash
bash reports/evaluation/common_core_v0/runs/calcite_hep_pg40_execution_01/run_manual_calcite_hep_pg40_execution.sh
```

The script is human-run only.
It uses PostgreSQL only.

## What The Script Does

For each executable row:

1. creates an isolated schema
2. loads `ddl_pg.sql`
3. loads `pg_witness_data.sql`
4. runs source SQL
5. runs generated Calcite SQL
6. exports TSV outputs
7. compares outputs
8. writes `result_check.json`
9. drops the isolated schema

## Caveats

- generation failures remain in the denominator and are represented as non-executed rows
- `PORT_0024 / pg` remains executable but carries `control_native_source_status=skipped`
- `PORT_0004` is missing `validation/pg_witness_data.sql`, but that row is already generation-failed and therefore not an execution target

## Out Of Scope

- no timing
- no speedup
- no leaderboard
