# Calcite HEP MySQL/Spark Execution/Validity Canary 02 Plan

## Scope

This package prepares a bounded human-run execution/validity canary for the six
rewrite-success rows produced by
`calcite_hep_mysql_spark_canary_02`.

Identifiers:

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `source_rewrite_run_id = calcite_hep_mysql_spark_canary_02`
- `execution_denominator_id = calcite_hep_mysql_spark_canary_02_rewrite_success_6`
- planned rows = `6`

Rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## Goal

Execute source SQL and generated Calcite HEP SQL against the labeled target
engine and compare exact TSV outputs.

## Important metadata rule

This package does **not** trust the blank `schema_path` fields retained in
`calcite_hep_mysql_spark_canary_02/run_event_long.csv`.

Instead it resolves schema and witness paths directly from the case package:

- MySQL schema:
  - `cases/<POOL>/<CASE>/schema/ddl_mysql.sql`
- Spark schema:
  - `cases/<POOL>/<CASE>/schema/ddl_spark.sql`
- MySQL witness:
  - `cases/<POOL>/<CASE>/validation/mysql_witness_data.sql`
- Spark witness:
  - `cases/<POOL>/<CASE>/validation/spark_witness_data.sql`

## Boundary

This package is validity-only:

- no timing
- no speedup
- no leaderboard
- no method-comparison update

Execution success alone is still narrower than paper-facing cross-method metric
integration. Existing PG-only Calcite HEP evidence remains canonical until this
canary is human-run and separately triaged.

## Expected row outcomes

Each row should record:

- `execution_status`
  - `executed`
  - `source_execution_failed`
  - `generated_execution_failed`
  - `setup_failed`
  - `comparison_failed`
- `consistency_status`
  - `match_exact`
  - `mismatch`
  - `not_applicable`

## Engine execution path

MySQL rows:

- source `scripts/env_mysql.sh`
- use MySQL CLI
- load schema and witness
- execute source and generated SQL
- capture TSV outputs

Spark rows:

- source `scripts/env_spark.sh`
- use inline PySpark
- load schema and witness statements into a temporary local warehouse
- execute source and generated SQL
- capture TSV outputs

## Package-level outputs

- `run_results.json`
- `run_event_long.csv`

## Row-level outputs

- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `metadata/<CASE>/<engine>/row_metadata.json`
