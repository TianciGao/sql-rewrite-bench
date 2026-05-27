# Calcite HEP 120 Recovery Canary 08 01

This package is a bounded, fail-closed recovery canary for eight low-risk
Calcite HEP ledger-gap rows identified in
`reports/evaluation/common_core_v0/calcite_hep_120_recovery_priority_v1.csv`.

It is human-run only. Codex must not execute it.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous fail-closed exact ledger: `70/120`
- planned rows: `8`

Target rows only:

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`
- `PERF_0008:mysql`
- `PERF_0013:mysql`
- `PERF_0017:mysql`
- `PERF_0019:mysql`
- `PERF_0077:spark`

## Recovery families

- PG DDL timestamp-ingestion repair:
  - `LONGTAIL_0022:pg`
  - `LONGTAIL_0023:pg`
  - `LONGTAIL_0024:pg`
- MySQL DDL table-name ingestion repair:
  - `PERF_0008:mysql`
  - `PERF_0013:mysql`
  - `PERF_0017:mysql`
  - `PERF_0019:mysql`
- Spark schema setup comment-only DDL fragment repair:
  - `PERF_0077:spark`

## Boundaries

- No database, Java, Calcite, PostgreSQL, MySQL, or Spark execution should be
  performed by Codex while preparing this package.
- No SQLGlot transpilation.
- No PostgreSQL fallback for MySQL or Spark.
- No semantic relaxation of exact-match.
- No semantic-failure rows, checker-only rows, or `PORT` rows are included.
- A row counts as recovered only if it produces retained `match_exact`
  validity evidence.

## Output contract

The runner writes:

- `run_results.json`
- `run_event_long.csv`
- `generated/<CASE>/<engine>/calcite_hep_recovery_rewrite.sql`
- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `metadata/<CASE>/<engine>/row_metadata.json`

## Claim boundary

`calcite_hep_120_recovery_canary_only_not_timing_speedup_or_leaderboard_evidence`
