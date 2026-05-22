# Calcite HEP 120 Recovery Round-4b Numeric Scale Canary 04 01 Plan

## Purpose

Retry only the four PostgreSQL and Spark rows that already execute but still
mismatch because retained generated SQL collapses engine-specific decimal
display scale in the final projection.

## Planned Rows

- `PERF_0062:pg`
- `PERF_0062:spark`
- `LONGTAIL_0013:pg`
- `LONGTAIL_0013:spark`

## Retained Mismatch Being Targeted

- `PERF_0062:pg`
  - retained source TSV uses `16` fractional digits for the first three numeric
    outputs and `2` for the fourth
- `PERF_0062:spark`
  - retained source TSV uses `1` fractional digit for the first numeric output,
    `6` for the next two, and `2` for the fourth
- `LONGTAIL_0013:pg`
  - retained source TSV uses `16` fractional digits for the average-like output
- `LONGTAIL_0013:spark`
  - retained source TSV uses `1` fractional digit for the average-like output

## Package Change

- use retained generated SQL from prior PG and Spark Calcite HEP runs
- create package-local repaired generated SQL copies before execution
- preserve engine-specific decimal display scale using SQL-level final
  projection casts only
- use the existing PostgreSQL and Spark env scripts
- execute source SQL and repaired generated SQL
- compare outputs exactly under the unchanged checker

## Expected Ledger Outcomes

- previous ledger: `86/120`
- `0` recovered => `86/120`
- `1` recovered => `87/120`
- `2` recovered => `88/120`
- `3` recovered => `89/120`
- `4` recovered => `90/120`

## Explicit Non-Goals

- no Calcite rerun
- no checker changes
- no TSV normalization
- no timing or speedup
- no paper-table or synthesis update in this task
