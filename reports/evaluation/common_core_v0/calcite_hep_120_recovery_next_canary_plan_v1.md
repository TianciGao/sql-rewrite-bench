# Calcite HEP 120 Recovery Next Canary Plan v1

## Purpose

Test only the lowest-risk retained recovery family rows from the Calcite HEP 120-row fail-closed ledger. This plan intentionally excludes semantic failures, checker-policy rows, and PORT-family methodology-boundary rows.

## Candidate Rows

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`
- `PERF_0008:mysql`
- `PERF_0013:mysql`
- `PERF_0017:mysql`
- `PERF_0019:mysql`
- `PERF_0077:spark`

## Family Coverage

- Spark setup artifact family: `PERF_0077:spark`
- MySQL DDL table-name ingestion family: `PERF_0008:mysql`, `PERF_0013:mysql`, `PERF_0017:mysql`, `PERF_0019:mysql`
- PG DDL timestamp-ingestion family: `LONGTAIL_0022:pg`, `LONGTAIL_0023:pg`, `LONGTAIL_0024:pg`

## Success Criterion

A row only counts as recovered if it moves from its current fail-closed non-exact state to retained `match_exact` validity evidence. Rewrite-only recovery or executability without exact-match does not increase the fail-closed ledger.

## Explicit Exclusions

- No semantic-failure rows
- No checker-only representation rows
- No PORT-family rows
- No timing or speedup steps

## Expected Maximum Upside

- at most `+8` exact rows
- fail-closed ledger ceiling after this canary: `78/120`
