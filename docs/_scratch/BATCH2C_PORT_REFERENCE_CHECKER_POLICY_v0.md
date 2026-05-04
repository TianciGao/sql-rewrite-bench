# Status

This note defines the bounded Batch 2C PORT PostgreSQL reference / checker policy for:

- `PORT_0013`
- `PORT_0016`
- `PORT_0024`
- `PORT_0025`

It is a scratch policy note only.

It does not modify case files.

It does not decide translation correctness.

# Policy Basis

Current Batch 2C PORT preflight shows that these four cases are structurally close to a bounded PostgreSQL route-matrix expansion, but they still need an explicit reference / checker policy before execution.

The main policy lessons from the existing PORT packet are:

- use `rewrite_pos_01.sql` as the primary reference when it is already PostgreSQL-compatible
- allow a report-local PostgreSQL-normalized reference only when the human positive reference is semantically intended but not PostgreSQL-compatible as written
- preserve exact TSV as the raw diagnostic result
- allow normalized TSV only when the difference is formatting-only rather than value-changing
- keep the full translation-correctness boundary explicit

# Per-Case Policy Table

| case_id | reference_sql_source | checker_policy | expected normalization needs | matrix eligibility | rationale |
| --- | --- | --- | --- | --- | --- |
| `PORT_0013` | `rewrite_pos_01.sql` | `exact_tsv_report_local` | `type cast normalization`, `boolean/null normalization`, `identifier quoting` | `ready_after_policy` | positive reference is already PostgreSQL-shaped and uses `DOUBLE PRECISION`; the main portability question is source-route boolean coercion rather than reference incompatibility |
| `PORT_0016` | `rewrite_pos_01.sql` | `diagnostic_only` | `date/time function normalization`, `identifier quoting` | `diagnostic_only` | positive reference is PostgreSQL-shaped, but this case is explicitly a date/time fairness case and should stay under diagnostic review first |
| `PORT_0024` | `rewrite_pos_01.sql` | `normalized_tsv_report_local` | `numeric formatting only`, `boolean/null normalization`, `identifier quoting` | `ready_after_policy` | positive reference is PostgreSQL-compatible; likely differences are numeric rendering around percentage computation, so normalized TSV should be allowed if exact output differs only by formatting |
| `PORT_0025` | `rewrite_pos_01.sql` | `exact_tsv_report_local` | `date/time function normalization`, `identifier quoting` | `ready_after_policy` | positive reference is PostgreSQL-shaped with `EXTRACT` and timestamp cast already in place; exact TSV is the right first check |

# Per-Case Notes

## PORT_0013

Observed source / reference shape:

- source SQL uses MySQL boolean aggregation and `CAST(... AS DOUBLE)`
- `rewrite_pos_01.sql` already rewrites this to PostgreSQL-compatible `DOUBLE PRECISION`

Policy decision:

- `reference_sql_source = rewrite_pos_01.sql`
- `checker_policy = exact_tsv_report_local`

Reason:

- this case does not need the `PORT_0012` style report-local PostgreSQL reference normalization step
- the main candidate-route risk is boolean/type semantics on the translated candidate, not reference incompatibility

## PORT_0016

Observed source / reference shape:

- source SQL uses `DATE_FORMAT` over `CAST(... AS DATETIME)`
- `rewrite_pos_01.sql` already maps this to PostgreSQL `EXTRACT(...) FROM CAST(... AS TIMESTAMP)`

Policy decision:

- `reference_sql_source = rewrite_pos_01.sql`
- `checker_policy = diagnostic_only`

Reason:

- reference SQL itself looks PostgreSQL-compatible
- this case remains fairness-sensitive because date/time semantics are the main portability focus
- it should remain outside the first clean Batch 2C matrix subset until that fairness policy is explicitly accepted

## PORT_0024

Observed source / reference shape:

- source SQL uses MySQL-style percentage computation with `CAST(... AS DOUBLE)`
- `rewrite_pos_01.sql` rewrites to `100.0 * SUM(...) / COUNT(...)`

Policy decision:

- `reference_sql_source = rewrite_pos_01.sql`
- `checker_policy = normalized_tsv_report_local`

Reason:

- the reference is already PostgreSQL-compatible
- the output is a percentage expression, so formatting-only numeric differences are plausible
- raw exact TSV should still be recorded first
- normalized TSV may then be used if the only difference is numeric formatting rather than value divergence

## PORT_0025

Observed source / reference shape:

- source SQL uses `DATE_FORMAT(..., '%Y') = '1993'`
- `rewrite_pos_01.sql` already maps that to PostgreSQL `EXTRACT(YEAR FROM CAST(... AS TIMESTAMP)) = 1993`

Policy decision:

- `reference_sql_source = rewrite_pos_01.sql`
- `checker_policy = exact_tsv_report_local`

Reason:

- positive reference is already PostgreSQL-compatible
- the first bounded check should remain exact TSV
- if later diagnostics show numeric-formatting-only or ordering-only differences, normalized TSV can be added explicitly rather than assumed now

# Recommended Batch 2C Execution Subset

Ready after policy freeze:

- `PORT_0013`
- `PORT_0024`
- `PORT_0025`

Diagnostic-only for the next lane:

- `PORT_0016`

Blocked outside this note and still needing separate backfill:

- `PORT_0003`
- `PORT_0006`

# Recommended Checker Policy

- default to `rewrite_pos_01.sql` as the PostgreSQL reference when it is already PostgreSQL-compatible
- allow report-local PostgreSQL-normalized references only when `rewrite_pos_01.sql` is semantically intended but not PostgreSQL-compatible as written
- preserve exact TSV as the raw diagnostic result in all cases
- use `normalized_tsv_report_local` only when the difference is formatting-only, especially numeric rendering
- keep any normalized-reference or normalized-TSV result labeled as bounded PG-side reference consistency only

# Boundaries

- PostgreSQL only
- reference/checker policy only
- not SQL execution
- not translation correctness
- not cross-engine closure
- not denominator expansion by itself
- no case-local rewrite modifications
- no registry update
- no formal review update
