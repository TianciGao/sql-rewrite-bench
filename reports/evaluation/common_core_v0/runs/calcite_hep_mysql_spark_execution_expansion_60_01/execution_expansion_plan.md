# Calcite HEP MySQL/Spark Execution-Validity Expansion 60 Plan

## Scope

This package prepares human-run execution and strict exact-match validity checks
for the `60` `rewrite_success` rows retained by:

- `run_id = calcite_hep_mysql_spark_rewrite_expansion_80_01`
- `path = reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_rewrite_expansion_80_01`

Identifiers:

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `source_rewrite_run_id = calcite_hep_mysql_spark_rewrite_expansion_80_01`
- `execution_denominator_id = calcite_hep_mysql_spark_execution_expansion_60_only`

Planned rows:

- `60` total
- `28` MySQL
- `32` Spark

## Inclusion Rule

Only rows with `row_status = rewrite_success` from the completed rewrite
expansion are eligible.

The package must not include:

- `parser_failed` rows
- `hep_rewrite_failed` rows
- rows missing source SQL
- rows missing generated SQL
- rows missing schema SQL
- rows missing witness data

## Boundary

This package is execution-validity only:

- no timing
- no speedup
- no leaderboard artifacts
- no update to `method_comparison_summary_v2`

Claim boundary:

- `mysql_spark_execution_validity_expansion_60_only_not_timing_speedup_or_leaderboard_evidence`

## Execution Contract

Per row, the human-run script must:

- build an isolated workspace
- copy `source.sql`
- copy retained `generated.sql`
- copy engine-specific DDL
- copy engine-specific witness data
- execute source and generated SQL on the target engine
- write `source.tsv`
- write `generated.tsv`
- write `result_check.json`
- write stdout/stderr logs
- write row metadata

Strict comparison is required:

- source output vs generated output
- exact TSV equality only

## Status Contract

Per row:

- `execution_status`:
  - `executed`
  - `source_execution_failed`
  - `generated_execution_failed`
  - `setup_failed`
  - `comparison_failed`
- `consistency_status`:
  - `match_exact`
  - `mismatch`
  - `not_applicable`

## Spark Artifact Hygiene

Spark warehouse or parquet artifacts must not be retained in the git-tracked
package tree.

The runner therefore uses a temporary warehouse under `/tmp` and removes it
before the row finishes.
