# Method Comparison Summary v2 Paper Readiness Check

## Verdict

- `paper_ready = yes`

This table is safe to use as a **denominator-aware paper result table** if it is presented as a comparison ledger or pre-leaderboard table, not as a single scalar leaderboard.

## Blocking Issues

- none

## Checks

### CSV Integrity

- CSV row widths are consistent: `yes`
- header width: `31`
- data rows: `6`

### Required Denominator / Scope Columns

All required columns exist:

- `generation_or_route_denominator_id`
- `execution_or_ready_denominator_id`
- `timing_denominator_id`
- `engine_scope`
- `denominator_caveat`
- `leaderboard_comparable`

### R-Bot Scope Check

R-Bot is represented correctly:

- `generation_or_route_denominator_id = common_core_v0_40_same_engine_120`
- `execution_or_ready_denominator_id = generated_pg7_only`
- `timing_denominator_id = generated_pg7_match_exact_only`
- `engine_scope = pg_subset_only`
- `leaderboard_comparable = no`

The markdown also states that R-Bot is subset-scoped and not full `120`-row timing or tri-engine evidence.

### Calcite HEP Scope Check

Calcite HEP is represented correctly:

- `engine_scope = pg_only`
- `leaderboard_comparable = no`

The surrounding source summaries and the v2 row both keep Calcite HEP clearly PG-only / PG40-only.

### Generalization Placeholder Check

These columns exist for all rows:

- `cross_engine_executable_rate`
- `cross_engine_consistency_rate`
- `speedup_transfer_rate`

Current representation is correct:

- all are `NA_not_computed`
- none are incorrectly written as `0`

### Negative Rejection Rate Check

- `negative_rejection_rate` exists for all rows
- it is `NA_not_computed` where unavailable
- it is not incorrectly written as `0`

### Leaderboard Overclaim Check

- No row with `leaderboard_comparable = no` is described as a winner, best method, or primary leaderboard result.
- Markdown warning language is explicit:
  - not a single scalar leaderboard
  - different route structures, engine scopes, and timing denominators
  - `leaderboard_comparable = no` means not directly rank-comparable without denominator normalization

### Support / Diagnostic Metric Check

- support / diagnostic metrics are present only as schema placeholders
- they are not used as ranking fields in the markdown table

## Warnings

### Warning 1

The compact markdown table still places `gm_speedup` and `regression_rate_20pct` side by side across non-comparable rows. The warning text is strong enough, but a paper caption should repeat that these are denominator-aware fields, not normalized leaderboard values.

### Warning 2

`leaderboard_comparable = no` is set for every row. This is correct and safe, but it means the table should be framed as an evidence ledger or scoped comparison summary, not as a ranked method table.

### Warning 3

`negative_rejection_rate` and all generalization primary metrics are still `NA_not_computed`. That is the correct representation, but the paper should avoid implying those dimensions were quantitatively compared.

## Recommended Wording Fixes

Recommended caption-style wording:

`Table X reports denominator-aware method evidence for Common-core v0. Rows are not directly rank-comparable unless denominator, route structure, engine scope, and timing scope align. In particular, Calcite HEP is PostgreSQL-only on a PG40 denominator, and R-Bot timing is available only for the generated_pg7_match_exact_only subset rather than a full same-engine denominator.`

Recommended in-text wording:

`We therefore use Table X as a scoped evidence table rather than a single scalar leaderboard.`

## Bottom Line

`method_comparison_summary_v2` can be used as a paper table **if**:

- it is described as denominator-aware
- it is not presented as a ranked leaderboard
- the caption or nearby text repeats the subset-scope caveats for Calcite HEP and R-Bot
