# Calcite HEP MySQL/Spark Execution/Validity Canary 02

This package prepares a bounded human-run execution/validity canary for the six
rewrite-success rows from
[calcite_hep_mysql_spark_canary_02](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/run_results.json).

Rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## Boundary

This package is validity-only:

- executes source SQL and generated SQL
- compares outputs
- does not compute timing
- does not compute speedup
- does not update method comparison tables

## Engine entrypoints

- MySQL rows source `scripts/env_mysql.sh`
- Spark rows source `scripts/env_spark.sh`

## Important path rule

This package resolves schema and witness paths directly from case directories.
It does not trust the blank `schema_path` values retained in
`calcite_hep_mysql_spark_canary_02/run_event_long.csv`.

## Output contract

For each row, the human-run package should write:

- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `metadata/<CASE>/<engine>/row_metadata.json`

Package-level outputs:

- `run_results.json`
- `run_event_long.csv`
