# SQLGlot Transpile Same-Dialect Noop Result Card v1

This is a paper-facing route card for one retained SQLGlot route only. It does
not update `method_comparison_summary_v2` in this task.

## Route Identity

| field | value |
|---|---|
| `method_id` | `sqlglot` |
| `route_id` | `sqlglot_transpile_same_dialect_noop` |
| `denominator_id` | `common_core_v0_40_same_engine_120_transpile_noop_route` |
| `engines` | `pg,mysql,spark` |
| `planned_rows` | `120` |
| `generated_rows` | `78` |
| `executed_rows` | `72` |
| `exact_match_rows` | `72` |
| `exact_among_executed` | `72/72` |
| `timing_denominator_id` | `timing_success_72_on_transpile_noop_route` |
| `leaderboard_comparable` | `no` |

## Claim Boundary

`SQLGlot transpile_same_dialect_noop is a same-engine 120-row route-level evidence row. It is denominator-aware route evidence, not cross-dialect portability evidence, not a full SQLGlot method-family aggregate, and not a leaderboard-comparable scalar. Unsupported, failed, and no-op rows remain explicit in denominator accounting.`

## Paper-Facing Counts

- fail-closed exact ledger on this route denominator: `72/120`
- generated: `78/120`
- executed: `72/120`
- exact among executed: `72/72`
- timing exists only on `timing_success_72_on_transpile_noop_route`

## Interpretation

- This route should be surfaced as a route-level same-engine row, not as a
  full SQLGlot family summary.
- This route should not be presented as cross-dialect portability evidence just
  because explicit PORT rows remain in denominator accounting.
- Unsupported, failed, and no-op rows remain visible in the route denominator.

## Source Artifacts

- [sqlglot_paper_route_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_paper_route_audit_v1.md)
- [sqlglot_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_validity_summary_v1.md)
- [sqlglot_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_speedup_summary_v1.md)
- [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
