# Direct LLM And LLM Translate 120 Readiness Audit v1

## Scope

This is a read-only evidence audit for Common-core v0 same-engine `120`-row
readiness.

Audited route candidates:

1. Direct LLM rewrite
2. LLM Translate

This audit does not run new generation, execution, checker, timing, or speedup
work. It does not update `method_comparison_summary_v2`. It does not create a
result card, proposed row, or leaderboard row.

## Executive Conclusion

- `direct_llm_same_engine_rewrite` has retained denominator-aware same-engine
  route evidence on the frozen Common-core v0 denominator.
- That Direct LLM route is already strong enough for a **main same-engine
  evidence-table row**, but it remains **not leaderboard-comparable** because
  timing is subset-scoped and denominator caveats remain explicit.
- `llm_translate` does **not** have a retained Common-core v0 same-engine
  `120`-row route packet.
- Retained `llm_translate` references are bounded portability-only evidence and
  should not be promoted into Track A same-engine readiness.

## Route Distinction

The retained artifacts support a clean distinction:

- `Direct LLM rewrite` is a retained same-engine Common-core v0 route:
  - `method_id = direct_llm`
  - `route_id = direct_llm_same_engine_rewrite`
- `LLM Translate` is not retained here as a same-engine Common-core v0 route:
  - current governance references only bounded portability-side evidence
  - no retained same-engine `120` route id, run packet, result card, or timing
    packet was found

So these should be audited as **separate routes / tracks**, not merged into one
LLM family readiness claim.

## Direct LLM Readiness

Retained artifacts used:

- [direct_llm_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.md)
- [direct_llm_validity_summary_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.csv)
- [direct_llm_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.md)
- [direct_llm_speedup_summary_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.csv)
- [direct_llm_same_engine_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_same_engine_result_card_v1.md)
- [direct_llm_same_engine_proposed_row_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_same_engine_proposed_row_v1.md)
- [METHOD_STATUS_LEDGER.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv)

Recovered route identity:

- `method_id = direct_llm`
- `route_id = direct_llm_same_engine_rewrite`
- result-card label present: `direct_llm_same_engine_result_card_v1`
- denominator id present: `common_core_v0_40`

Recovered counts:

- planned rows: `120`
- generated rows: `120`
- source executed rows: `115`
- candidate / generated executed rows: `99`
- exact-match rows: `94`
- timing rows: `94`
- speedup rows: `94`

Failure buckets:

- `preflight_blocked = 5`
- `execution_failed = 16`
  - `llm_generated_sql_dialect_execution_failure = 14`
  - `draft_ddl_package_limitation = 2`
- `mismatch = 5`

Engine representation:

- PostgreSQL represented: `40`
- MySQL represented: `40`
- Spark represented: `40`

Protocol interpretation:

- Checker protocol is retained and aligned enough for a same-engine
  denominator-aware evidence row on the executed subset.
- Timing protocol is also retained, but only on the
  `timing_success_94_on_common_core_v0_40` subset.
- Therefore Direct LLM is **main-table eligible as a denominator-aware
  same-engine route row**, but **not leaderboard-comparable**.

Exact missing evidence for stronger claims:

- no full-denominator `120/120` timing packet
- no justification to treat subset timing as a final ranked scalar
- explicit blocked / failed / mismatch rows remain part of denominator
  accounting

## LLM Translate Readiness

Retained artifacts used:

- [METHOD_STATUS_LEDGER.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv)
- [DECISION_NOTES.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/DECISION_NOTES.md)
- [EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.md)
- [EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv)
- [sqlglot_paper_route_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_paper_route_audit_v1.md)

Recovered current status:

- `method_id = llm_translate`
- retained same-engine `route_id`: `UNKNOWN_NOT_RECOVERED`
- retained same-engine result card label: none found
- retained same-engine denominator id: none found

What is retained:

- bounded portability-only references on `port_bounded_6`
- PG-side bounded packet noted as `6/6` success
- no retained MySQL/Spark same-engine packet
- no retained Common-core v0 `120` same-engine route packet

So for Common-core v0 `120` readiness:

- planned rows: `NA_not_retained_common_core_v0_120_route`
- generated rows: `NA_not_retained_common_core_v0_120_route`
- source executed rows: `NA_not_retained_common_core_v0_120_route`
- candidate executed rows: `NA_not_retained_common_core_v0_120_route`
- exact-match rows: `NA_not_retained_common_core_v0_120_route`
- timing rows: `0`
- speedup rows: `NA_not_computed`

Protocol interpretation:

- checker protocol is not retained for a same-engine `120` packet
- timing protocol is not retained for a same-engine `120` packet
- all three engines are not represented
- the route is therefore **not enough evidence** for Common-core v0 same-engine
  `120` readiness

Exact missing evidence:

- dedicated same-engine `route_id`
- retained generation packet on the `40 x 3 = 120` denominator
- retained execution / checker packet on that denominator
- retained timing packet on that denominator
- retained paper-facing result card or proposed row for that same-engine route

## Route-Level Summary

| route_label | method_id | route_id | planned | generated | source_executed | candidate_executed | exact | timing | speedup | eligibility |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Direct LLM rewrite | `direct_llm` | `direct_llm_same_engine_rewrite` | `120` | `120` | `115` | `99` | `94` | `94` | `94` | `main_table_eligible_same_engine_evidence_only_not_leaderboard_comparable` |
| LLM Translate | `llm_translate` | `UNKNOWN_NOT_RECOVERED` | `NA` | `NA` | `NA` | `NA` | `NA` | `0` | `NA` | `not_enough_evidence_for_common_core_v0_120_readiness` |

## Eligibility Decision

### Direct LLM rewrite

- main-table eligible: `yes`
- leaderboard-comparable: `no`
- exact next separate gate:
  - no new result card or proposed row is needed because both already exist
  - the next separate gate would be a human paper-admission decision on whether
    to keep the retained denominator-aware Direct LLM route row in the main
    same-engine evidence table with its existing caveats

### LLM Translate

- main-table eligible: `no`
- appendix-only or exclude:
  - for this Common-core v0 `120` same-engine audit, it should be treated as
    **not enough evidence**
  - bounded portability references may still remain usable in a separate
    portability appendix, but they are not Track A same-engine readiness

## Paper-Safe Statements

Direct LLM:

`Direct LLM rewrite has retained denominator-aware same-engine Common-core v0 evidence on 120 planned rows, with 120 generation successes, 99 executed rows, 94 exact matches, and subset-scoped timing on 94 rows. This supports a main same-engine evidence-table row with explicit denominator caveats, but not a leaderboard-comparable scalar.`

LLM Translate:

`No retained Common-core v0 same-engine 120-row LLM Translate route packet was recovered. Existing references remain bounded portability-only evidence and should not be promoted into Track A same-engine readiness claims.`

## Non-Claims

- No new generation was run.
- No PostgreSQL / MySQL / Spark run was executed.
- No checker, timing, or speedup run was executed.
- No result card was created.
- No proposed row was created.
- No leaderboard row was created.
- `method_comparison_summary_v2` remains unchanged.
