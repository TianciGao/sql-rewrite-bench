# Common-core v0 Metric Readiness Matrix

This matrix separates what is ready from the current controls package versus what would require actual method leaderboard or support-track artifacts.

## Headline

- Controls validity coverage is ready to report now on the frozen `common_core_v0_40` denominator.
- Controls validity coverage is not a method leaderboard.
- Performance metrics remain blocked on runtime-bearing method runs.
- Cross-engine leaderboard metrics remain blocked on explicit PORT translation packages.
- Plan-observability and verifier-support metrics remain separate support layers and are not yet materialized for Common-core v0.

## Matrix

| metric_name | metric_layer | current_status | can_report_now | can_use_for_method_ranking | denominator | source_artifact | caveat | next_gap |
|---|---|---|---|---|---|---|---|---|
| executable_rate | primary_validity | ready_controls_only | yes | no | common_core_v0_40 | `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv` | Controls-only benchmark validity coverage, not method ranking | Build same-engine method raw and derived leaderboard tables |
| result_consistency_rate | primary_validity | ready_controls_only | yes | no | common_core_v0_40 | `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv` | Controls-only source-vs-positive consistency evidence; unsupported PORT native-source rows remain explicit | Materialize denominator-aware method result summaries |
| negative_rejection_rate | primary_validity | ready_controls_only | yes | no | common_core_v0_40 | `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv` | Controls-only hard-negative evidence | Build method-level negative-control reporting from evaluated rewrites |
| gm_speedup | primary_performance | not_ready | no | no | common_core_v0_40 | `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md` | No timing-bearing method rows exist yet | Run same-engine method evaluations with runtime capture |
| regression_rate@20% | primary_performance | not_ready | no | no | common_core_v0_40 | `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md` | No denominator-complete runtime deltas are materialized | Publish method case summaries with baseline/rewrite runtime deltas |
| cross_engine_executable_rate | primary_generalization | partial_old_evidence | no | no | common_core_v0_40 | `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv` | PORT controls are benchmark support only, not translation leaderboard output | Materialize `port_translation_summary` from actual cross-engine methods |
| cross_engine_consistency_rate | primary_generalization | partial_old_evidence | no | no | common_core_v0_40 | `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv` | Existing PORT controls do not establish method translation consistency rankings | Run denominator-aware cross-engine method result packages |
| speedup_transfer_rate | primary_generalization | not_ready | no | no | common_core_v0_40 | `benchmark_spec/reviews/COMMON_CORE_V0_FINAL_FREEZE_REVIEW.md` | Freeze review explicitly blocks default SpeedupTransferRate claims from PORT normalization-caveat rows | Collect explicit cross-engine runtime-transfer artifacts with separated caveat framing |
| verifier_support_rate | verifier_support | not_ready | no | no | common_core_v0_40 | `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md` | Verifier support must remain separate from same-engine leaderboard reporting | Create explicit verifier-support run packages and summaries |
| plan_parse_rate | plan_observability_support | not_ready | no | no | common_core_v0_40 | `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md` | No Common-core v0 plan package is materialized in the current evidence set | Run plan collection and publish `plan_observability_summary` |
| node_alignment_coverage | plan_observability_support | not_ready | no | no | common_core_v0_40 | `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md` | No denominator-complete node-alignment package is materialized | Produce node-alignment artifacts and coverage summaries |
| attribution_coverage | plan_observability_support | not_ready | no | no | common_core_v0_40 | `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md` | Attribution support depends on missing plan-delta/alignment outputs | Produce attribution-ready plan observability outputs |

## Readiness Interpretation

### Ready now

- `executable_rate`
- `result_consistency_rate`
- `negative_rejection_rate`

These are ready only as controls-level denominator-aware benchmark validity signals, using the combined controls status package:

- `324` fresh manual validation rows
- `36` explicit skipped unsupported rows
- `0` missing rows

That means controls coverage is denominator-complete across `40 x 3 x 3 = 360` case/engine/route rows, with unsupported PORT combinations kept explicit rather than dropped.

### Not ready for ranking

No metric in this matrix is currently ready for method ranking.

The current artifact base is controls-first:

- it proves benchmark support and validity scaffolding
- it does not yet provide same-engine method leaderboard outputs
- it does not yet provide cross-engine method translation summaries
- it does not yet provide plan-observability or verifier-support packages

### Main next steps

1. Run denominator-complete same-engine method evaluations with runtime capture.
2. Materialize `method_case_summary` and `same_engine_leaderboard`.
3. Materialize explicit `port_translation_summary` for cross-engine methods.
4. Materialize separate `verifier_support_summary`.
5. Materialize separate `plan_observability_summary`.
