# SQLGlot Optimize Same-Dialect Result Card v1

This is a paper-facing route card for one retained SQLGlot route only. It does
not update `method_comparison_summary_v2` in this task.

## Route Identity

| field | value |
|---|---|
| `method_id` | `sqlglot` |
| `route_id` | `sqlglot_optimize_same_dialect` |
| `denominator_id` | `common_core_v0_40_same_engine_120_optimize_route` |
| `engines` | `pg,mysql,spark` |
| `planned_rows` | `120` |
| `generated_rows` | `75` |
| `executed_rows` | `65` |
| `exact_match_rows` | `65` |
| `fail_closed_exact_ledger` | `65/120` |
| `exact_among_executed` | `65/65` |
| `timing_denominator_id` | `timing_success_65_on_optimize_route` |
| `leaderboard_comparable` | `no` |

## Denominator Treatment

- generation_failed rows remain explicit: `27`
- noop_generated rows remain explicit: `0`
- skipped_unsupported rows remain explicit: `18`
- executed failure rows remain explicit: `10`

These rows are not dropped from denominator accounting.

## Claim Boundary

`SQLGlot optimize_same_dialect is a same-engine route-level evidence row. It is denominator-aware route evidence, not cross-dialect portability evidence, not a full SQLGlot method-family aggregate, and not a leaderboard-comparable scalar unless retained timing/speedup evidence explicitly supports that boundary.`

## Paper-Facing Counts

- fail-closed exact ledger on this route denominator: `65/120`
- generated: `75/120`
- executed: `65/120`
- exact among executed: `65/65`
- timing exists only on `timing_success_65_on_optimize_route`

## Final Paper-Safe Statement

`SQLGlot optimize_same_dialect is a same-engine route-level evidence row on a 120-row denominator. Retained artifacts support 75 generated rows, 65 executed rows, and a fail-closed exact ledger of 65/120, with 65/65 exact matches among executed rows. Unsupported, failed, and no-op rows remain explicit in denominator accounting. This is denominator-aware route evidence, not cross-dialect portability evidence, not a full SQLGlot method-family aggregate, and not a leaderboard-comparable scalar.`

## Source Artifacts

- [sqlglot_paper_route_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_paper_route_audit_v1.md)
- [sqlglot_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_validity_summary_v1.md)
- [sqlglot_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_speedup_summary_v1.md)
- [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
