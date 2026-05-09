# Method Comparison Summary v2 Paper Readiness Check v2

## Verdict

- `paper_ready = yes`

The updated `method_comparison_summary_v2` is safe to use as a
**denominator-aware evidence ledger** in the paper if it is described as a
scoped comparison table rather than a ranked leaderboard.

## Blocking Issues

- none

## Checks

### CSV Integrity

- CSV row widths are consistent: `yes`
- header width: `31`
- data rows: `6`

### Required Denominator / Scope Columns

All required columns are present and explicit for every row:

- `generation_or_route_denominator_id`
- `execution_or_ready_denominator_id`
- `timing_denominator_id`
- `engine_scope`
- `denominator_caveat`
- `leaderboard_comparable`

### Leaderboard Comparability

- `leaderboard_comparable = no` for all rows
- there is no explicit justification in the current canonical table for any row
  to be treated as fully rank-comparable
- this remains conservative and paper-safe

### R-Bot Scope Check

R-Bot is represented correctly after the PG expansion v2 update:

- `generation_or_route_denominator_id = common_core_v0_40_pg40`
- `execution_or_ready_denominator_id = generated_pg15_from_pg40_expansion_only`
- `timing_denominator_id = generated_pg15_from_pg40_expansion_match_exact_only`
- `engine_scope = pg_only`
- `leaderboard_comparable = no`

The markdown also states that:

- the row is PostgreSQL-only
- the timing evidence is subset-scoped
- the earlier PG7 evidence remains historical provenance

### R-Bot Overclaim Check

The updated R-Bot row does **not** present its `GM_Speedup` as:

- full PG40 timing
- full `120` same-engine timing
- tri-engine timing
- leaderboard evidence

That boundary is explicit both in:

- `method_comparison_summary_v2.md`
- the row-local `denominator_caveat`
- the row-local `caveat`
- R-Bot v2 supporting summaries

### Historical Provenance Check

The updated R-Bot row preserves historical PG7 provenance:

- `reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.md`
- `reports/evaluation/common_core_v0/r_bot_pg7_speedup_summary_v1.md`

Those links remain in `source_summary_files`, so the replacement is not a loss
of auditability.

### Generalization Placeholder Check

These columns are present for all rows:

- `cross_engine_executable_rate`
- `cross_engine_consistency_rate`
- `speedup_transfer_rate`

Current representation remains correct:

- all are `NA_not_computed`
- none are incorrectly written as `0`

### Negative Rejection Rate Check

- `negative_rejection_rate` exists for all rows
- it remains `NA_not_computed` where unavailable
- it is not incorrectly written as `0`

### Winner / Ranking Language Check

- No row with `leaderboard_comparable = no` is described as a winner, best
  method, or primary leaderboard result.
- Markdown still warns that the table is **not** a single scalar leaderboard.
- The updated R-Bot explanation remains framed as evidence visibility, not
  as a ranking claim.

### Support / Diagnostic Metric Check

- support / diagnostic metrics remain schema placeholders
- they are not used as ranking fields in the markdown table

## Warnings

### Warning 1

The compact markdown table still places `gm_speedup` and
`regression_rate_20pct` side by side across rows that are not denominator- or
scope-matched. The table is safe, but the paper caption should restate that
these are denominator-aware evidence fields, not normalized leaderboard values.

### Warning 2

`leaderboard_comparable = no` remains true for every row. This is correct, but
it means the table should be framed as an evidence ledger or scoped comparison
summary, not as a ranked method table.

### Warning 3

`negative_rejection_rate` and all generalization primary metrics remain
`NA_not_computed`. The paper should not imply those dimensions were
quantitatively compared.

### Warning 4

The updated R-Bot row is newer and stronger than the historical PG7 row, but it
is still only PG-only subset timing evidence. Any narrative sentence must avoid
reading `GM_Speedup = 0.921825` as if it covered all PG40 rows or the full
`120`-row same-engine denominator.

## Recommended Paper Caption Wording

Recommended caption-style wording:

`Table X reports denominator-aware method evidence for Common-core v0. Rows are not directly rank-comparable unless denominator, route structure, engine scope, and timing scope align. In particular, Calcite HEP is PostgreSQL-only on a PG40 denominator, and R-Bot uses the newer PG expansion v2 evidence with timing available only for the generated_pg15_from_pg40_expansion_match_exact_only subset rather than full PG40 or full 120-row same-engine timing.`

Recommended in-text wording:

`We therefore use Table X as a scoped evidence ledger rather than a ranked leaderboard.`

## Bottom Line

`method_comparison_summary_v2` can be used in the paper as an evidence ledger.

It should **not** be used as a ranked leaderboard.
