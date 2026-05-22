# Calcite HEP 120 Recovery Round-3c Numeric Scale Canary 02 01 Plan

## Purpose

Retry only the two MySQL rows that already execute but still mismatch because
retained generated SQL renders numeric outputs without the source query's fixed
decimal display scale.

## Planned Rows

- `PERF_0062:mysql`
- `LONGTAIL_0013:mysql`

## Retained Mismatch Being Targeted

- `PERF_0062:mysql`
  - source TSV: `4.0000`, `120.000000`, `80.000000`, `80.00`
  - generated TSV: `4`, `120`, `80`, `80.00`
- `LONGTAIL_0013:mysql`
  - source TSV includes `5.0000` and `4.0000`
  - generated TSV includes `5` and `4`

## Package Change

- use retained Round-3 generated MySQL SQL as input
- create a package-local repaired generated SQL copy before execution
- preserve decimal display scale using SQL-level final projection casts only
- use existing `MYSQL_DATABASE` from `scripts/env_mysql.sh`
- perform explicit row-local table cleanup before schema load and after row completion
- execute source SQL and repaired generated SQL
- compare outputs exactly under the unchanged checker

## Expected Ledger Outcomes

- previous ledger: `84/120`
- `0` recovered => `84/120`
- `1` recovered => `85/120`
- `2` recovered => `86/120`

## Explicit Non-Goals

- no rewrite rerun outside the retained Round-3 generated SQL
- no checker changes
- no TSV normalization
- no timing or speedup
- no paper-table or synthesis update in this task
