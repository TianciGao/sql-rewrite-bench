# R-Bot PG1 Execution Canary 01

This package prepares a human-run PostgreSQL execution and validity check for the retained R-Bot PG1 exploratory generation result on `PERF_0006`.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- planned rows: `1`

## Boundary

- exploratory PG1 recovery evidence only
- `current_benchmark_metric_evidence = false`
- claim boundary:
  - `exploratory_smoke_only_not_current_common_core_metric_evidence`
- no timing
- no speedup
- no leaderboard
- no case or registry modification

## How To Run

From repo root:

```bash
bash reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/run_manual_r_bot_pg1_execution_canary.sh
```

The script is human-run only.
Codex must not execute it.

## What The Script Does

1. sources `scripts/env_postgres.sh`
2. runs `python -m scripts.cli pg-check`
3. creates an isolated PostgreSQL schema for the row
4. loads `ddl_pg.sql`
5. loads `pg_witness_data.sql`
6. runs the frozen source SQL
7. runs the retained generated R-Bot SQL
8. writes `source.tsv` and `generated.tsv`
9. compares TSV outputs by exact text equality only
10. writes `result_check.json`
11. writes `run_results.json`
12. drops the isolated schema in cleanup

## Failure Semantics

- if PostgreSQL preflight fails, the row remains explicit as `not_executed_preflight_failed`
- if source or generated SQL execution fails, the row remains explicit as `execution_failed`
- if outputs differ, the row remains explicit as `mismatch`
- success remains exploratory only and must not be upgraded into current benchmark metric evidence

## Inputs

- [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json)
- [r_bot_pg_rewrite.sql](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/source.sql)
- [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/schema/ddl_pg.sql)
- [pg_witness_data.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/validation/pg_witness_data.sql)

## Outputs After Human Execution

- `logs/pg_check.stdout.log`
- `logs/pg_check.stderr.log`
- `logs/perf_0006__pg__r_bot_pg_rewrite.stdout.log`
- `logs/perf_0006__pg__r_bot_pg_rewrite.stderr.log`
- `workspaces/PERF_0006/pg/r_bot_pg_rewrite/source.tsv`
- `workspaces/PERF_0006/pg/r_bot_pg_rewrite/generated.tsv`
- `workspaces/PERF_0006/pg/r_bot_pg_rewrite/result_check.json`
- `records.tmp.jsonl`
- `run_results.json`
