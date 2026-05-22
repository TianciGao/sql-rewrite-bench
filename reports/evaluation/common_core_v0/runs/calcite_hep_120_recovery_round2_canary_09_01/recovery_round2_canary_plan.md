# Calcite HEP 120 Recovery Round 2 Canary 09 01 Plan

## Purpose

Attempt only the retained round-2 low-risk implementation candidates from the
Calcite HEP `120`-row fail-closed ledger.

## Planned rows

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`
- `PERF_0062:mysql`
- `PERF_0062:spark`
- `LONGTAIL_0012:mysql`
- `LONGTAIL_0012:spark`
- `LONGTAIL_0013:mysql`
- `LONGTAIL_0013:spark`

## Implementation-level repairs only

1. PostgreSQL quoted mixed-case identifier normalization after rel-to-SQL so
   generated SQL resolves against lowercase physical tables created by unquoted
   DDL.
2. AVG / decimal scale preservation after Calcite render so generated SQL keeps
   engine-native numeric formatting under the existing exact-match checker.

## Success rule

A row only counts as recovered if it moves from its current fail-closed
non-exact state to retained `match_exact` validity evidence.

## Expected upside

- previous fail-closed exact ledger: `75/120`
- maximum recoverable rows in this canary: `9`
- ceiling after this canary: `84/120`

## Explicit exclusions

- no semantic-failure rows
- no checker-policy normalization
- no `PORT` rows
- no timing or speedup
