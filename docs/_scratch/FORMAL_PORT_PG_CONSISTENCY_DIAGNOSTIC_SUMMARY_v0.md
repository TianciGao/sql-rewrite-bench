# FORMAL_PORT_PG_CONSISTENCY_DIAGNOSTIC_SUMMARY_v0

## 1. Status

This is a tracked scratch diagnostic over existing PORT PostgreSQL materialized TSVs, checker outputs, and reference SQL files.

This is diagnostic-only and does not rerun SQL, regenerate SQL, or claim translation correctness.

## 2. Why Diagnostic Was Needed

The earlier exact-TSV PORT PG reference check produced three non-consistent outcomes:

- SQLGlot `PORT_0004`
- SQLGlot `PORT_0022`
- Direct LLM `PORT_0022`

It also exposed a reference-SQL execution failure on Direct LLM `PORT_0012`.

The diagnostic was needed to separate:

- true value mismatches
- formatting-only mismatches
- reference SQL incompatibility on the PostgreSQL side

## 3. SQLGlot Mismatch Analysis

Observed executable SQLGlot cases:

- `PORT_0004`
  - exact byte equal: `false`
  - row count equal: `true`
  - normalized equal: `false`
  - mismatch guess: `true_value_difference_unknown`
  - diff sample: reference `50.0` vs candidate `\N`
- `PORT_0022`
  - exact byte equal: `false`
  - row count equal: `true`
  - normalized equal: `false`
  - mismatch guess: `true_value_difference_unknown`
  - diff sample: reference `0.25000000000000000000` vs candidate `0.0`

Diagnostic interpretation:

- SQLGlot mismatches do not collapse under safe normalization.
- The current SQLGlot PORT PG inconsistencies look like actual result divergence, not byte-format noise.

## 4. LLM Mismatch Analysis

Observed LLM cases with available TSV pairs:

- `PORT_0004`
  - exact byte equal: `true`
  - normalized equal: `true`
  - result: exact match
- `PORT_0022`
  - exact byte equal: `false`
  - row count equal: `true`
  - normalized equal: `true`
  - mismatch guess: `numeric_formatting_only`
  - diff sample: reference `0.25000000000000000000` vs candidate `0.25`

Diagnostic interpretation:

- The LLM `PORT_0022` mismatch appears to be numeric formatting only.
- Under a safe normalization pass, the LLM executable cases with available TSV pairs close to `2 / 2`.

## 5. PORT_0012 Reference SQL Issue

`PORT_0012` should not currently be treated as a candidate-route value mismatch in the PORT PG reference checker.

Observed reference SQL issue:

- file: `cases/PORT/PORT_0012/rewrite_pos_01.sql`
- classification: `reference_sql_not_pg_compatible`
- signals:
  - `uses_AS_DOUBLE_cast_not_supported_by_postgres`
  - `uses_YEAR_function_not_native_postgres`

Route interpretation:

- SQLGlot `PORT_0012` remained blocked before reference checking because route PG execution had already failed with `InvalidDatetimeFormat`.
- Direct LLM `PORT_0012` reference checking failed because the current positive reference SQL itself was not PostgreSQL-compatible.

This means the current LLM `PORT_0012` consistency failure is a reference-layer problem, not evidence of a candidate mismatch.

## 6. Exact vs Normalized Comparison Result

Across available TSV pairs:

- exact checked pair count: `4`
- exact consistent: `1`
- exact inconsistent: `3`
- normalized checked pair count: `4`
- normalized consistent: `2`
- normalized inconsistent: `2`

Net effect:

- normalization changes only one observed mismatch category:
  - Direct LLM `PORT_0022` moves from exact mismatch to normalized match
- normalization does not rescue SQLGlot `PORT_0004`
- normalization does not rescue SQLGlot `PORT_0022`
- normalization cannot close `PORT_0012` while the current PG reference SQL remains incompatible

## 7. Recommended Checker Policy

Recommended checker policy:

- `reference_sql_pg_normalization_needed`

Reasoning:

- a normalized checker is helpful for formatting-only cases such as Direct LLM `PORT_0022`
- but the larger blocker is the reference layer itself, especially `PORT_0012`
- SQLGlot still shows apparent true value divergence even after normalization

## 8. Recommended Next Action

- implement normalized PORT PG reference checker only if diagnostics show byte mismatches are formatting/order-only; otherwise keep exact TSV result and record true mismatch candidates

Current implication:

- Direct LLM `PORT_0022` is the only current candidate for normalization-based closure
- SQLGlot mismatches should remain visible as likely true mismatches
- `PORT_0012` needs PostgreSQL-compatible reference-SQL treatment before route-vs-reference consistency can be interpreted cleanly

## 9. Boundaries

- diagnostic only
- not translation correctness
- not MySQL / Spark
- not cross-engine closure
- not full PORT closure
- no registry writeback
- no formal review update

