# Method Comparison Consistency Audit v1

## Verdict

`method_comparison_summary_v1` is **not yet safe to use as a paper-facing comparison table without caveated explanation**.

Main reasons:

1. `calcite_hep` denominator-aware evidence exists in standalone summaries but is **absent** from `method_comparison_summary_v1`.
2. denominator labeling improved materially after the R-Bot addition, but the comparison table still lacks explicit schema fields for:
   - `engine_scope`
   - `denominator_caveat`
3. primary-method metric coverage is incomplete:
   - `negative_rejection_rate` is not represented
   - generalization primary metrics are not represented as explicit `NA_not_computed` fields
   - `speedup_transfer_rate` is absent instead of explicitly marked `NA_not_computed`
4. the table is conservative about `leaderboard_comparable_without_denominator_labels`, which is good, but that does not by itself close the schema gap.

## High-Level Findings

### Passes

- Existing rows do carry explicit denominator IDs for generation/route, execution/ready, and timing scope.
- Existing rows do **not** mix benchmark-support diagnostics into ranking columns.
- Existing rows do **not** silently coerce R-Bot PG7 timing into full-denominator timing.
- `leaderboard_comparable_without_denominator_labels = no` is correct for every current row.

### Warnings

- `engine_scope` is still implicit rather than a first-class column.
- `denominator_caveat` is encoded only indirectly through `denominator_note` and `evidence_note`.
- `attempted_or_ready_rows` remains semantically overloaded across methods:
  - SQLGlot: attempted
  - Direct LLM: ready-to-execute
  - R-Bot: generated subset execution denominator

### Fails

- `calcite_hep` is missing from the comparison table even though denominator-aware validity and speedup summaries exist.
- `speedup_transfer_rate` is not represented.
- `cross_engine_executable_rate` and `cross_engine_consistency_rate` are not represented.
- `negative_rejection_rate` is not represented.
- Uncomputed generalization metrics are absent rather than explicitly marked `NA_not_computed`.

## Denominator Audit

### SQLGlot

- Denominator awareness is strong in both standalone validity and speedup summaries.
- In the comparison table, route and timing denominators are explicit.
- Remaining issue: `engine_scope` is implicit, and the combined SQLGlot row is structurally different from single-route rows.

### Direct LLM

- Denominator awareness is strong in standalone summaries.
- Comparison row is explicit enough to prevent accidental flattening into SQLGlot combined rows.
- Remaining issue: missing explicit `engine_scope`, `denominator_caveat`, and missing generalization-metric placeholders.

### Calcite HEP

- Standalone summaries are denominator-aware and clearly PG-only on `common_core_v0_40_pg40`.
- The comparison table does not include it, so readers cannot see denominator mismatch at the comparison layer.
- This is the largest omission in the current comparison package.

### R-Bot

- Standalone summaries are denominator-aware and correctly scoped.
- Comparison row preserves:
  - `generation_or_route_denominator_id = common_core_v0_40_same_engine_120`
  - `execution_or_ready_denominator_id = generated_pg7_only`
  - `timing_denominator_id = generated_pg7_match_exact_only`
- The row is therefore safe as **subset evidence**, but not as full-denominator timing evidence.

## Metric Audit

### Validity / Same-Engine

Present in the comparison table:

- executable-rate style metrics: `yes`
- result-consistency-rate style metrics: `yes`

Missing:

- `negative_rejection_rate`: `missing`

### Performance

Present in the comparison table:

- `gm_speedup`: `yes`
- `regression_rate@20%`: `yes`

### Generalization

Expected primary metrics:

- `cross_engine_executable_rate`
- `cross_engine_consistency_rate`
- `speedup_transfer_rate`

Current state:

- all three are `missing from schema`
- they should be represented as `NA_not_computed` until aligned cross-engine evidence exists

### Support / Diagnostic Metrics

Checked:

- `verifier_support_rate`
- `plan_parse_rate`
- `node_alignment_coverage`
- `attribution_coverage`

Current state:

- not mixed into the current comparison leaderboard-like table
- this is correct

## NA vs Zero Audit

### Good

- R-Bot subset timing is not falsely shown as full-denominator coverage.
- Existing rows do not use `0` to stand in for R-Bot’s absent full-denominator timing.
- Standalone method summaries generally keep unsupported and blocked rows visible rather than silently dropping them.

### Not Good Enough

- Generalization primary metrics are absent instead of explicitly marked `NA_not_computed`.
- That omission leaves room for later accidental interpretation as “not considered” rather than “considered but not yet computed”.

## Row-Level Audit

| method_id | route_id | row status | denominator fields | primary metrics | support metrics mixed into leaderboard | comparability flag | severity | recommended fix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sqlglot` | `sqlglot_combined_same_engine` | present | `generation_or_route_denominator_id`, `execution_or_ready_denominator_id`, `timing_denominator_id` present; `engine_scope` missing; `denominator_caveat` missing as discrete field | executable/result-consistency/performance present; `negative_rejection_rate` missing; generalization metrics missing | `no` | correct (`no`) | `warning` | add `engine_scope`, `denominator_caveat`, `negative_rejection_rate`, and explicit `NA_not_computed` generalization columns |
| `sqlglot` | `sqlglot_optimize_same_dialect` | present | same issue pattern as above | same issue pattern as above | `no` | correct (`no`) | `warning` | same as above |
| `sqlglot` | `sqlglot_transpile_same_dialect_noop` | present | same issue pattern as above | same issue pattern as above | `no` | correct (`no`) | `warning` | same as above |
| `direct_llm` | `direct_llm_same_engine_rewrite` | present | denominator IDs present; `engine_scope` missing; `denominator_caveat` missing as discrete field | executable/result-consistency/performance present; `negative_rejection_rate` missing; generalization metrics missing | `no` | correct (`no`) | `warning` | add missing schema columns and explicit `NA_not_computed` generalization fields |
| `r_bot` | `r_bot_same_engine_rewrite` | present | denominator IDs present and especially important; `engine_scope` still missing; `denominator_caveat` only implicit | executable/result-consistency/performance present in subset form; `negative_rejection_rate` missing; generalization metrics missing | `no` | correct (`no`) | `warning` | keep row, but add explicit `engine_scope = pg_subset_only`, `denominator_caveat`, and `NA_not_computed` generalization fields |
| `calcite_hep` | `calcite_hep_pg_rewrite` | missing from comparison table | cannot audit row-level denominator labeling because row absent | standalone primary metrics exist, but comparison row absent | `no` | not applicable because missing | `fail` | add a denominator-aware Calcite row with explicit `engine_scope = pg_only`, `denominator_id = common_core_v0_40_pg40`, and `leaderboard_comparable_without_denominator_labels = no` |

## Comparability Audit

Current comparability flags are conservative and correct:

- SQLGlot combined row: `no`
- SQLGlot route rows: `no`
- Direct LLM row: `no`
- R-Bot row: `no`

This is the right choice because:

- SQLGlot combined uses a `240`-row aggregate of two routes
- Direct LLM uses a single `120`-row same-engine route
- R-Bot uses a `120`-row generation denominator but only a `PG7` timing subset
- Calcite, once added, will be `PG40` only

No current row should be treated as cross-row leaderboard-comparable without an explicit denominator-normalization policy.

## Speedup Transfer Rate Audit

Current state: **incorrectly represented by omission**.

That is:

- `speedup_transfer_rate` is not claimed
- but it is also not present as `NA_not_computed`

Recommended representation:

- add `speedup_transfer_rate`
- value: `NA_not_computed`
- reason: aligned source-target validity and timing evidence is not yet available across methods

## Recommended Next Action

Do **not** treat `method_comparison_summary_v1` as a final paper table.

Next action:

1. create `method_comparison_summary_v2`
2. add explicit schema fields for:
   - `engine_scope`
   - `denominator_caveat`
   - `negative_rejection_rate`
   - `cross_engine_executable_rate`
   - `cross_engine_consistency_rate`
   - `speedup_transfer_rate`
3. populate uncomputed generalization metrics as `NA_not_computed`
4. add denominator-aware `calcite_hep` row
5. keep `leaderboard_comparable_without_denominator_labels = no` unless and until denominator and engine scope are aligned
