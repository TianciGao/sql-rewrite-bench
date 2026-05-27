# Calcite HEP MySQL/Spark Execution Expansion 60

This package prepares a bounded human-run execution-validity expansion for the
`60` retained `rewrite_success` rows from:

- `calcite_hep_mysql_spark_rewrite_expansion_80_01`

## Scope

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `execution_denominator_id = calcite_hep_mysql_spark_execution_expansion_60_only`
- planned rows = `60`
- engines:
  - `mysql = 28`
  - `spark = 32`

## Boundary

This package is not:

- timing evidence
- speedup evidence
- leaderboard evidence
- a method comparison update

It executes only the retained `rewrite_success` rows and checks exact output
equality.

## Spark Hygiene

Spark rows use a temporary warehouse under `/tmp` and clean it before row exit.
Only retained TSV, JSON, SQL copies, logs, metadata, and summaries remain under
the package directory.
