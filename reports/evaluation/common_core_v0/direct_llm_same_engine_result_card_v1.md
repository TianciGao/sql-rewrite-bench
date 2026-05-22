# Direct LLM Same-Engine Result Card v1

This is a paper-facing route card for retained Direct LLM same-engine rewrite
evidence only. It does not update `method_comparison_summary_v2` in this task.

## Route Identity

| field | value |
|---|---|
| `method_id` | `direct_llm` |
| `route_id` | `direct_llm_same_engine_rewrite` |
| `evidence_type` | `route_summary` |
| `denominator_id` | `common_core_v0_40` |
| `engine_scope` | `tri_engine_same_engine` |
| `planned_rows` | `120` |
| `generated_or_ready_rows` | `115` |
| `executed_rows` | `99` |
| `exact_match_rows` | `94` |
| `fail_closed_exact_ledger` | `94/120` |
| `exact_among_executed` | `94/99` |
| `timing_success_rows` | `94` |
| `timing_denominator_id` | `timing_success_94_on_common_core_v0_40` |
| `gm_speedup` | `1.0436` |
| `regression_rate_20pct` | `0.0319` |
| `leaderboard_comparable` | `no` |

## Failure Accounting

- `unsupported_rows`: `UNKNOWN_NOT_RECOVERED`
- `parse_failed_rows`: `UNKNOWN_NOT_RECOVERED`
- `generation_failed_rows`: `0`
- `noop_rows`: `UNKNOWN_NOT_RECOVERED`
- `preflight_blocked_rows`: `5`
- `execution_failed_rows`: `16`
- `mismatch_rows`: `5`
- `methodology_boundary_rows`: `UNKNOWN_NOT_RECOVERED`

Interpretation boundary:

- `preflight_blocked` rows are package or artifact gaps and are not counted as
  generated-SQL failures in the retained validity summary
- `execution_failed` and `mismatch` remain explicit denominator rows
- PORT rows retain portability-stress caveats and must not be normalized into a
  cross-dialect claim

## Paper-Facing Counts

- fail-closed exact ledger: `94/120`
- generated or ready to execute: `115/120`
- executed: `99/120`
- exact among executed: `94/99`
- timing exists only on `timing_success_94_on_common_core_v0_40`

## Source Artifacts Used

- [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
- [direct_llm_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.md)
- [direct_llm_validity_summary_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.csv)
- [direct_llm_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.md)
- [direct_llm_speedup_summary_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.csv)

## Paper-Safe Statement

`Direct LLM same-engine rewrite is a denominator-aware same-engine route row on the common_core_v0_40 denominator. Retained artifacts support 115 ready-to-execute rows, 99 executed rows, and a fail-closed exact ledger of 94/120, with 94/99 exact matches among executed rows. Timing and GM speedup are retained only on the timing_success_94_on_common_core_v0_40 subset. This is same-engine route evidence, not cross-dialect portability evidence, not a final ranked leaderboard scalar, and not direct proof that denominator-misaligned rows are rank-comparable.`

## Explicit Non-Claims

- This result card does not create a leaderboard.
- This result card does not update `method_comparison_summary_v2`.
- This result card does not convert the row into canonical status by itself.
- This result card does not claim cross-dialect portability evidence.
- This result card does not claim that subset-scoped timing metrics are
  full-denominator leaderboard scalars.
