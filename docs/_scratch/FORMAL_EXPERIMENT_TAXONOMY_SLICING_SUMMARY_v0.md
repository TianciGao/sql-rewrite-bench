# FORMAL_EXPERIMENT_TAXONOMY_SLICING_SUMMARY_v0

## 1. Status

This is the first formal experiment taxonomy / feature slicing summary built from existing metadata and existing result artifacts only.

It is not taxonomy writeback.

It is not final RQ4.

## 2. Inputs Inspected

- `reports/formal_common_core/failure_slicing_preflight_v0.json`
- `reports/formal_common_core/control_scoring_v0.json`
- `reports/formal_common_core/method_consistency_scoring_v0.json`
- `reports/formal_common_core/method_speedup_scoring_v0.json`
- `reports/formal_common_core/plan_operator_delta_summary_v0.json`
- `reports/formal_port/port_current_results_snapshot_v0.json`
- `inventory/case_registry.csv`
- case-local `manifest.yaml` where present
- case-local `taxonomy_trial*.yaml` where present
- tracked taxonomy definition files under `taxonomy/`

## 3. Metadata / Taxonomy Coverage

- total cases aggregated: `12`
- common-core cases: `9`
- PORT snapshot cases: `3`
- metadata records read: `18`
- taxonomy records read: `11`
- cases with some taxonomy / tag coverage: `12`
- cases fully untagged: `0`

Current caveat:

- tag coverage exists, but quality is uneven
- several cases rely on manifest tags without a usable taxonomy trial file
- some taxonomy trial files are placeholders or explicitly provisional

## 4. Common-Core Slicing By Pool / Source Family

Pool split:

- performance: `7`
- consistency: `2`

Source-family split:

- `TPC-H`: `5`
- `TPC-DS`: `2`
- `Calcite`: `2`

Current interpretation:

- the current common-core packet remains dominated by analytical performance cases
- consistency slicing is currently a small Calcite-derived subline

## 5. Slicing By SQL Feature / Rewrite Opportunity

Observed SQL feature buckets:

- `date_time_function`: `8`
- `correlated_subquery`: `3`
- `expression_complexity`: `3`
- `subquery_in_from`: `2`
- `untagged`: `2`

Observed rewrite-opportunity buckets:

- `predicate_pushdown`: `7`
- `join_reorder`: `4`
- `dialect_adaptation`: `3`
- `function_normalization`: `3`
- `materialization_strategy`: `3`
- `subquery_decorrelation`: `3`
- `expression_simplification`: `2`
- `order_limit_simplification`: `1`

Current interpretation:

- the current packet already supports a useful paper-facing split between:
  - analytical predicate / join optimization cases
  - subquery / decorrelation consistency cases
  - dialect-adaptation portability cases

## 6. Plan Operator / Plan-Observability Slicing

Observed plan-operator buckets:

- `scan`: `12`
- `aggregate`: `12`
- `join`: `9`
- `sort`: `7`
- `limit`: `5`
- `filter`: `3`
- `subquery`: `2`
- `materialize`: `1`

Plan-observability interpretation:

- all common-core cases remain plan-observable in the current packet
- plan-operator tags are available for every aggregated case
- operator-delta remains an observation layer only, not attribution

## 7. PORT / Portability Slicing

PORT denominator split:

- clean snapshot:
  - `PORT_0004`
  - `PORT_0022`
- holdout failure-analysis:
  - `PORT_0012`

Observed portability-tag buckets:

- `datetime_semantics_gap`: `8`
- `type_semantics_gap`: `4`
- `identifier_quoting`: `3`
- `limit_fetch_gap`: `1`
- `untagged`: `3`

Current interpretation:

- date/time portability remains the strongest cross-case portability theme in the current packet
- `PORT_0012` remains the anchor failure case for portability translation risk

## 8. Failure / Blocker Bucket Slicing

Common-core buckets:

- `generated_method_checker_backed_consistency_closed`: `9`
- `operator_delta_observed_not_attribution`: `9`
- `attribution_not_computed`: `9`
- `registry_admission_not_claimed`: `9`
- `perf_only_speedup_completed`: `7`
- `speedup_policy_frozen`: `7`
- `cons_excluded_from_gm_speedup`: `2`

PORT buckets:

- `full_port_closure_not_claimed`: `3`
- `registry_admission_not_claimed`: `3`
- `port_invalid_datetime_format`: `1`
- `quoted_identifier_vs_string_literal_confusion`: `1`
- `datetime_timestamp_formatting`: `1`
- `dialect_normalization_failure`: `1`
- `portability_translation_failure`: `1`
- `port_holdout_failure_analysis`: `1`

## 9. Claim Eligibility Slicing

- `main_table_correctness`: `9`
- `plan_observability`: `9`
- `main_table_perf_speedup`: `7`
- `not_yet_claimable`: `2`
- `port_snapshot`: `2`
- `failure_case_study`: `1`

Current interpretation:

- full common-core correctness and plan-observability eligibility are closed
- speedup eligibility remains intentionally PERF-only
- PORT is split into clean snapshot evidence and one explicit failure-study case

## 10. Metadata Gaps / Taxonomy Gaps

- taxonomy trial missing: `6`
- taxonomy trial placeholder or empty: `5`
- taxonomy trial provisional: `1`
- SQL feature tag gaps: `2`
- portability tag gaps: `3`
- workload realism tag gaps: `2`

Important caveat:

- feature-level slicing is only as complete as current manifest tags and trial tags
- missing or provisional tags are being reported, not repaired

## 11. RQ4 Interpretation

- a usable first-pass RQ4 slicing layer now exists
- the current packet is strong enough to support:
  - pool-level slicing
  - source-family slicing
  - feature-bucket slicing
  - rewrite-opportunity slicing
  - plan-operator slicing
  - blocker / failure-bucket slicing
- this is still not final taxonomy closure

## 12. Remaining Work

- turn the slicing output into a paper-facing RQ4 table draft
- decide whether placeholder trial files should be ignored or normalized in later reporting
- refine feature-level coverage rates after tag quality review
- keep attribution and leaderboard packaging separate

## 13. Claim Boundaries

- this is not taxonomy writeback
- this is not registry writeback
- this is not final RQ4
- missing or provisional tags are reported, not fixed
- feature-level rates are only as complete as current metadata
- no new metrics were computed
- no experiments were run

## 14. Recommended Next Action

- produce a paper-facing RQ4 coverage/failure table draft from the taxonomy slicing output, keeping missing/provisional tag caveats explicit
