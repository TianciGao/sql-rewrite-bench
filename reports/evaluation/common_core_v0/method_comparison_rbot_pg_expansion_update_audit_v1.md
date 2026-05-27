# Method Comparison R-Bot PG Expansion Update Audit v1

## Goal

Audit how the newer denominator-aware R-Bot PostgreSQL expansion evidence
should be integrated into `method_comparison_summary_v2` without turning a
subset-scoped row into a misleading leaderboard row.

## Current R-Bot Row

Current `method_comparison_summary_v2` R-Bot row:

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `evidence_type = pg_subset_route_summary`
- `generation_or_route_denominator_id = common_core_v0_40_same_engine_120`
- `execution_or_ready_denominator_id = generated_pg7_only`
- `timing_denominator_id = generated_pg7_match_exact_only`
- `engine_scope = pg_subset_only`
- `planned_generation_or_route_rows = 120`
- `generated_or_ready_rows = 7`
- `executed_rows = 7`
- `match_exact_rows = 7`
- `timing_success_rows = 7`
- `gm_speedup = 0.947444`
- `regression_rate_20pct = 0.2857`
- `leaderboard_comparable = no`

This row is correct as retained historical evidence, but it is no longer the
latest denominator-aware R-Bot evidence.

## Candidate Update Policies

### Option A: Replace the current R-Bot row with PG expansion v2

Pros:

- keeps one row per `method_id + route_id`
- avoids two R-Bot rows with different subset scopes competing in the same
  comparison table
- makes the table reflect the newest retained R-Bot evidence
- still allows historical PG7 links to remain in provenance fields

Cons:

- the canonical table no longer shows the PG7 row directly unless the user
  follows source links

### Option B: Keep the PG7 row and add a second R-Bot PG expansion v2 row

Pros:

- preserves both historical and newer subset rows directly in the table

Cons:

- two rows would share the same `method_id` and `route_id`
- `method_comparison_summary_v2` currently has no dedicated evidence-version
  column beyond `evidence_type`
- paper readers are more likely to misread this as two comparable R-Bot rows
  rather than historical-vs-latest evidence

## Recommended Policy

Recommended policy: `A. replace`.

Reason:

`method_comparison_summary_v2` is supposed to be a safer paper-facing comparison
ledger, not a historical archive. For the same `method_id` and `route_id`,
keeping only the newest denominator-aware row is safer than showing two
subset-scoped R-Bot rows side by side. Historical PG7 evidence should remain
retained through:

- `r_bot_formal_result_card_v1.md`
- `r_bot_pg7_speedup_summary_v1.md`
- `source_summary_files`
- `caveat`

## Proposed R-Bot PG Expansion v2 Row

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `method_family = r_bot`
- `evidence_type = pg_expansion_v2_route_summary`
- `generation_or_route_denominator_id = common_core_v0_40_pg40`
- `execution_or_ready_denominator_id = generated_pg15_from_pg40_expansion_only`
- `timing_denominator_id = generated_pg15_from_pg40_expansion_match_exact_only`
- `engine_scope = pg_only`
- `planned_generation_or_route_rows = 40`
- `generated_or_ready_rows = 15`
- `executed_rows = 15`
- `match_exact_rows = 15`
- `timing_success_rows = 15`
- `leaderboard_comparable = no`
- `executable_rate = 0.3750`
- `result_consistency_rate = 0.3750`
- `negative_rejection_rate = NA_not_computed`
- `gm_speedup = 0.921825`
- `regression_rate_20pct = 0.2000`
- `cross_engine_executable_rate = NA_not_computed`
- `cross_engine_consistency_rate = NA_not_computed`
- `speedup_transfer_rate = NA_not_computed`
- support / diagnostic metrics = `NA_not_computed`

## Safety Checks

- No row with `leaderboard_comparable = no` is described as a winner in the
  preview.
- `GM_Speedup` and `RegressionRate@20%` remain explicitly PG-only,
  denominator-scoped metrics.
- `speedup_transfer_rate` remains present and `NA_not_computed`.
- All denominator fields remain explicit.
- The preview keeps all non-R-Bot rows unchanged.

## Audit Conclusion

The safer update is to replace the current PG7-scoped R-Bot row with the newer
PG expansion v2 row in a later separate apply task, while preserving historical
PG7 provenance links inside the row notes and source-summary fields.
