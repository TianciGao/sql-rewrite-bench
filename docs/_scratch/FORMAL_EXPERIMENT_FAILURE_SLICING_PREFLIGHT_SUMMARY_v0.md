# FORMAL_EXPERIMENT_FAILURE_SLICING_PREFLIGHT_SUMMARY_v0

## 1. Status

This is the first RQ4-oriented failure / coverage slicing preflight built from existing formal common-core and PORT results only.

It is an aggregation layer only.

It is not final RQ4.

## 2. Inputs Inspected

- formal common-core closeout and rollup notes
- current paper experiment dashboard
- formal PORT current results snapshot
- `PORT_0012` failure-analysis packet
- full method consistency and method speedup scoring summaries
- plan operator-delta summary
- `reports/formal_common_core/control_scoring_v0.json`
- `reports/formal_common_core/method_consistency_scoring_v0.json`
- `reports/formal_common_core/method_speedup_scoring_v0.json`
- `reports/formal_common_core/plan_operator_delta_summary_v0.json`
- `reports/formal_port/port_current_results_snapshot_v0.json`
- `inventory/case_registry.csv`
- selected `manifest.yaml` and `taxonomy_trial*.yaml` paths when safely readable

## 3. Common-Core Slicing Summary

- common-core case count: `9`
- pool split:
  - performance: `7`
  - consistency: `2`
- generated-method checker-backed consistency closed count: `9`
- generated-method checker-backed consistency open count: `0`
- main-table correctness eligibility: `9`
- plan-observability eligibility: `9`
- PERF speedup eligibility: `7`
- consistency-semantic-only / not-yet-claimable for speedup: `2`

Current interpretation:

- RQ1 closure exists for the full 9-case common-core packet
- RQ2 observability closure exists at the parse / pair-ready / operator-delta-observation layer
- the current runtime packet is explicitly split:
  - PERF cases participate in current correctness-gated speedup
  - CONS cases remain excluded from `GM_Speedup`

## 4. PORT Slicing Summary

- PORT case count: `3`
- clean PORT denominator: `2`
  - `PORT_0004`
  - `PORT_0022`
- holdout failure-analysis case: `1`
  - `PORT_0012`
- current claim eligibility:
  - `current_port_snapshot`: `2`
  - `failure_case_study`: `1`

Current interpretation:

- a bounded clean PORT subset exists
- `PORT_0012` remains the central holdout failure-analysis case
- full PORT closure is still not claimable

## 5. Failure / Blocker Bucket Summary

Common-core blocker / boundary buckets:

- `generated_method_checker_backed_consistency_closed`: `9`
- `operator_delta_observed_not_attribution`: `9`
- `attribution_not_computed`: `9`
- `registry_admission_not_claimed`: `9`
- `perf_only_speedup_completed`: `7`
- `speedup_policy_frozen`: `7`
- `cons_excluded_from_gm_speedup`: `2`

PORT failure / blocker buckets:

- `full_port_closure_not_claimed`: `3`
- `registry_admission_not_claimed`: `3`
- `port_invalid_datetime_format`: `1`
- `quoted_identifier_vs_string_literal_confusion`: `1`
- `datetime_timestamp_formatting`: `1`
- `dialect_normalization_failure`: `1`
- `portability_translation_failure`: `1`
- `port_holdout_failure_analysis`: `1`

## 6. Claim Eligibility Summary

- common-core correctness main-table eligible: `9`
- common-core plan-observability eligible: `9`
- common-core PERF speedup eligible: `7`
- common-core not-yet-claimable for current speedup packet: `2`
- PORT current snapshot eligible: `2`
- PORT failure-case-study eligible: `1`

## 7. RQ4 Interpretation

- a first bounded blocker / failure bucket aggregation now exists
- the current result packet is strong enough to separate:
  - closed common-core correctness
  - closed common-core plan observability
  - closed PERF-only generated-method speedup
  - bounded PORT clean subset
  - explicit holdout failure-analysis
- this is still not final taxonomy slicing
- feature-level failure-rate slicing remains future work

## 8. Remaining Gaps

- taxonomy bucket aggregation is not final
- feature-level failure-rate slicing is not computed
- no registry or taxonomy tag writeback has been performed
- attribution remains uncomputed
- full PORT closure remains open
- leaderboard packaging remains separate

## 9. Claim Boundaries

- this is not final RQ4
- this is not registry writeback
- this is not taxonomy tag writeback
- this is not final leaderboard
- this is not admission
- this only aggregates current evidence and blockers

## 10. Recommended Next Action

- implement a formal taxonomy / feature slicing aggregation that joins current result records with case taxonomy tags, without changing registry or taxonomy files
