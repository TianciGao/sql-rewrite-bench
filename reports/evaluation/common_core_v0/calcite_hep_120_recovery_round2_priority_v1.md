# Calcite HEP 120 Recovery Round 2 Priority v1

Current fail-closed exact ledger: `75/120`.

This audit reviews only the retained round-2 candidate families requested for
inspection:

- PG execution-failure rows from recovery canary `08_01`
- non-PG numeric mismatch rows from the retained MySQL/Spark execution expansion

It does not relax exact-match semantics, does not normalize checker output, and
does not change denominator scope.

## Task A: PG Execution-Failure Triage

Rows inspected:

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`

Common retained evidence:

- the package-local recovery wrapper compiled successfully
- DDL ingestion succeeded
- Calcite parse / validate / SQL-to-rel / HEP / rel-to-SQL all succeeded
- target-dialect PostgreSQL SQL was emitted
- execution then failed under `psql`

Observed failure mechanism:

- generated SQL refers to quoted mixed-case relation names such as `"Posts"`,
  `"Comments"`, `"Users"`, `"PostLinks"`, and `"PostHistory"`
- case-local PostgreSQL DDL creates unquoted identifiers, so PostgreSQL stores
  them as lowercase physical names
- source SQL uses unquoted names and executes successfully
- generated SQL therefore fails at execution with relation-not-found errors

Classification:

- all three PG rows are best classified as
  `low-risk identifier/schema compatibility issue`
- this is narrower than a semantic SQL failure and narrower than a case artifact
  issue
- a bounded package-local render-side identifier normalization can be tested
  without changing case files or checker semantics

## Task B: Numeric Exact-Match Recovery Feasibility

Rows inspected:

- `PERF_0062:mysql`
- `PERF_0062:spark`
- `LONGTAIL_0012:mysql`
- `LONGTAIL_0012:spark`
- `LONGTAIL_0013:mysql`
- `LONGTAIL_0013:spark`

Observed retained mismatch pattern:

- source and generated outputs have the same row counts, row ordering, and
  column counts
- mismatches are confined to numeric string representation / scale
- examples:
  - `4.0000` vs `4`
  - `120.000000` vs `120`
  - `0.0000` vs `0`
  - `5.0` vs `5`
- retained generated SQL shows Calcite-rendered AVG-like expressions forced
  through `SIGNED`, `INTEGER`, or `DECIMAL(..., 0)` casts

Classification:

- all six non-PG rows are best classified as
  `exact same rows/columns but numeric scale/string-format loss`
- current retained evidence does not show output-shape change, ordering change,
  or semantic value change for these six rows
- because checker semantics are fixed, the only safe recovery path is a
  package-local Calcite render repair that preserves engine-native AVG / decimal
  scale in the generated SQL

## Round-2 Recommendation

A bounded round-2 canary is justified.

Recommended scope:

- PG identifier/schema compatibility family:
  - `LONGTAIL_0022:pg`
  - `LONGTAIL_0023:pg`
  - `LONGTAIL_0024:pg`
- non-PG numeric scale-preservation family:
  - `PERF_0062:mysql`
  - `PERF_0062:spark`
  - `LONGTAIL_0012:mysql`
  - `LONGTAIL_0012:spark`
  - `LONGTAIL_0013:mysql`
  - `LONGTAIL_0013:spark`

Maximum safe near-term upside from this round: `+9` exact rows.

- previous ledger: `75/120`
- round-2 ceiling if all selected rows recover exact-match validity:
  `84/120`

## Paper-Safe Wording If Round 2 Succeeds

`After a second bounded Calcite HEP recovery canary targeting identifier/schema compatibility on PostgreSQL and numeric scale-preservation on retained MySQL/Spark mismatch rows, the fail-closed exact-match ledger improved from 75/120 to X/120. Any recovered rows reflect implementation-level rendering or execution-compatibility repair, not relaxation of exact-match semantics, denominator scope, or checker policy.`

## Paper-Safe Wording If Round 2 Fails

`The second bounded Calcite HEP recovery canary did not convert the selected identifier/schema or numeric-scale rows into additional exact-match evidence. This strengthens the interpretation that the remaining 120-row fail-closed gaps are not low-risk implementation defects alone and should remain explicit non-exact denominator rows.`
