# Selected Plan Observability Frontier v1

## Purpose

这个文件回答什么问题：把 Section 8.7.3 的 selected observability frontier 做成 paper-facing ledger，明确它是 selected PG frontier evidence，而不是 full-denominator causal attribution。

## Selected frontier scope

- Preferred source is `table10_plan_attribution_case_study_v6.csv`.
- Frontier rows are selected PG plan-delta diagnostics plus one separate failure-side exemplar.
- The failure exemplar stays outside the exact-timed PG attribution denominator.
- Broader packet context from the retained `113`-row PG frontier remains: `aggregate_strategy_change:1|buffer_or_runtime_delta_without_operator_change:100|join_strategy_change:1|mixed_operator_change:6|node_count_change:2|scan_strategy_change:3` and confidence `low:102|medium:11`.

## Observability frontier table

| case_id | pool | method_id | route_id | outcome | speedup | delta_class | confidence | source_plan_available | rewrite_plan_available |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CONS_0007 | CONS | direct_llm | direct_llm_same_engine_rewrite | speedup | 1.3490894909920232 | join_strategy_change | medium | yes | yes |
| LONGTAIL_0011 | LONGTAIL | calcite_hep | calcite_hep_fail_closed_120 | regression | 0.782018801549 | scan_strategy_change | medium | yes | yes |
| LONGTAIL_0013 | LONGTAIL | calcite_hep | calcite_hep_fail_closed_120 | neutral | 0.999412588321 | node_count_change | medium | yes | yes |
| PORT_0012 | PORT | direct_llm | direct_llm_same_engine_rewrite | speedup | 1.265542934640196 | buffer_or_runtime_delta_without_operator_change | low | yes | yes |
| PERF_0035 | PERF | sqlglot | sqlglot_optimize_same_dialect | neutral | 0.9648371610687768 | mixed_operator_change | medium | yes | yes |
| CONS_0024 | CONS | direct_llm | direct_llm_same_engine_rewrite | failure_diagnostic | NA_failure_only | failure_diagnostic | none | no | no |

## Delta-class summary

- buffer_or_runtime_delta_without_operator_change=1; failure_diagnostic=1; join_strategy_change=1; mixed_operator_change=1; node_count_change=1; scan_strategy_change=1

## Confidence summary

- low=1; medium=4; none=1

## Failure exemplar summary

- `CONS_0024 / pg / direct_llm_same_engine_rewrite` remains a separate failure-side mismatch exemplar.
- It retains concrete `result_check` and stderr artifacts, but it is not merged into the exact-timed PG attribution frontier denominator.

## What this supports

- Selected-frontier observability for speedup, regression, neutral, mixed-operator, and failure diagnostics.
- Retained delta-class and confidence labels from the selected PG attribution packet.
- Failure-side diagnosis with a concrete retained mismatch exemplar.

## What this does not support

- Full 120-row NodeAlignmentCoverage.
- Denominator-wide plan-node causal attribution.
- Cross-engine plan attribution.
- Inferring causality from SQL text or prose alone.

## Safe prose snippet for the paper

Current evidence supports selected-frontier observability and failure attribution. Current evidence does not support full 120-row NodeAlignmentCoverage. Plan artifacts and delta classes help diagnose speedup, regression, no-op, mismatch, and execution failure, but they do not prove causal attribution across the full denominator.
