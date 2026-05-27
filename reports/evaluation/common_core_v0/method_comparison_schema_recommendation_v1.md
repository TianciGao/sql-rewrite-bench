# Method Comparison Schema Recommendation v1

## Goal

Define a cleaner `method_comparison_summary_v2` schema that separates:

- identifiers
- denominator/scope
- validity metrics
- performance metrics
- generalization metrics
- support/diagnostic metrics
- caveats

This should prevent subset-scoped rows such as R-Bot PG7 from being mistaken for full-denominator rows, and it should allow Calcite PG40 to coexist without false leaderboard comparability.

## Recommended v2 Column Groups

### 1. Identifiers

- `method_id`
- `method_group`
- `route_id`
- `route_scope`
- `evidence_version`

### 2. Denominator / Scope

- `generation_or_route_denominator_id`
- `generation_or_route_denominator_rows`
- `execution_denominator_id`
- `execution_denominator_rows`
- `timing_denominator_id`
- `timing_denominator_rows`
- `engine_scope`
- `pool_scope`
- `same_engine_scope`
- `tri_engine_scope`
- `denominator_caveat`
- `leaderboard_comparable_without_denominator_labels`

Recommended conventions:

- `engine_scope` examples:
  - `tri_engine_same_engine`
  - `pg_only`
  - `pg_subset_only`
- `denominator_caveat` should be a short machine-readable phrase, not only prose in a note field.

### 3. Validity Metrics

- `generation_success_rows`
- `generation_failed_rows`
- `blocked_rows`
- `unsupported_rows`
- `attempted_or_ready_rows`
- `attempted_or_ready_label`
- `executable_success_rows`
- `execution_failed_rows`
- `match_exact_rows`
- `mismatch_rows`
- `generation_success_rate_over_planned`
- `executable_rate_over_planned`
- `executable_rate_over_attempted_or_ready`
- `result_consistency_rate_over_planned`
- `result_consistency_rate_over_executed`
- `negative_rejection_rate`

Recommended convention:

- `negative_rejection_rate` should mean denominator-visible rejected or unusable rows for the method’s validity path.
- If a method has multiple rejection buckets, retain the detailed buckets elsewhere and publish one normalized rate here.

### 4. Performance Metrics

- `timing_success_rows`
- `coverage_over_planned`
- `coverage_over_timing_eligible`
- `gm_speedup`
- `median_speedup_ratio`
- `mean_speedup_ratio`
- `min_speedup_ratio`
- `p25_speedup_ratio`
- `p75_speedup_ratio`
- `max_speedup_ratio`
- `count_speedup_gt_1`
- `count_speedup_lt_1`
- `count_regression_lt_0_8`
- `regression_rate_at_20`

### 5. Generalization Metrics

- `cross_engine_executable_rate`
- `cross_engine_consistency_rate`
- `speedup_transfer_rate`
- `generalization_metric_status`

Recommended convention:

- if not computed, write `NA_not_computed`
- do **not** write `0` unless the metric was actually computed and equals zero
- include a status or note field such as:
  - `NA_not_computed`
  - `not_applicable_same_engine_only`
  - `computed`

### 6. Support / Diagnostic Metrics

These should be outside the ranking core but may still be useful:

- `verifier_support_rate`
- `plan_parse_rate`
- `node_alignment_coverage`
- `attribution_coverage`
- `artifact_contract_complete`
- `runtime_lock_status`

Recommended convention:

- keep these in separate grouped columns
- never use them as primary ranking fields in the main comparison narrative

### 7. Caveats / Provenance

- `port_caveat`
- `evidence_note`
- `provenance_note`
- `retry_or_replacement_note`
- `subset_scope_warning`

## Recommended Representation Rules

### NA vs Zero

- uncomputed metrics: `NA_not_computed`
- not applicable metrics: `NA_not_applicable`
- real measured zero: `0` or `0.0000`

### Denominator Matching

Rows should be comparable only when at least these align:

- `engine_scope`
- timing denominator semantics
- route granularity policy
- numerator definition for validity and timing

If these do not align:

- keep the row in the table
- set `leaderboard_comparable_without_denominator_labels = no`
- carry an explicit `denominator_caveat`

## Minimum v2 Upgrade Needed Now

To materially improve the current table:

1. add `engine_scope`
2. add `denominator_caveat`
3. add `negative_rejection_rate`
4. add:
   - `cross_engine_executable_rate`
   - `cross_engine_consistency_rate`
   - `speedup_transfer_rate`
5. fill uncomputed generalization metrics with `NA_not_computed`
6. add `calcite_hep` row with `engine_scope = pg_only`

That is enough to make the comparison package substantially safer for paper-facing use while still keeping it clearly pre-leaderboard.
