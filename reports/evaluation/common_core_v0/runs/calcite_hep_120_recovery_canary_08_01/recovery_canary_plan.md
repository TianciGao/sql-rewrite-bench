# Calcite HEP 120 Recovery Canary 08 01 Plan

## Purpose

Attempt only the eight low-risk recovery rows from the fail-closed
`70/120` Calcite HEP ledger, without relaxing denominator discipline or
exact-match semantics.

## Planned rows

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`
- `PERF_0008:mysql`
- `PERF_0013:mysql`
- `PERF_0017:mysql`
- `PERF_0019:mysql`
- `PERF_0077:spark`

## Implementation-level repairs only

The package-local wrapper and runner may repair only these retained failure
families:

1. PG DDL timestamp-ingestion brittleness
2. MySQL DDL table-name ingestion brittleness
3. Spark setup comment-only DDL fragment brittleness

No case SQL, schema SQL, witness SQL, or generated SQL is modified in-place.

## Success rule

A row increases the fail-closed ledger only if it reaches:

- rewrite produced nonempty target-engine SQL
- source SQL executed on the target engine
- generated SQL executed on the target engine
- `source.tsv == generated.tsv`

Anything less remains a non-exact denominator row.

## Expected upside

- previous fail-closed exact ledger: `70/120`
- maximum recoverable rows in this canary: `8`
- ceiling after this canary: `78/120`

## Explicit exclusions

- no semantic-failure rows
- no checker/representation-only rows
- no `PORT` rows
- no timing
- no speedup
- no leaderboard claims
