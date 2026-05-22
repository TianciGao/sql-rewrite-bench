# Candidate Failure Accounting v1

## Purpose

这个文件回答什么问题：把 method/route 输出的 non-exact frontier 和 failure buckets 做成 paper-facing route-level accounting，并和 hard-negative controls 明确分开。

## Route-level accounting table

| method_id | route_id | denominator_id | planned | generated_or_ready | executed | exact | non_exact_frontier | generation_failed | parse_failed | preflight_blocked | unsupported | execution_failed | mismatch | noop_or_source_like | timing_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| direct_llm | direct_llm_same_engine_rewrite | common_core_v0_40_same_engine_120 | 120 | 120 | 99 | 94 | 26 | 0 | 0 | 5 | 0 | 16 | 5 | 0 | 0 |
| direct_llm | direct_llm_execute_repair_1shot | common_core_v0_40_same_engine_120 | 120 | 120 | 97 | 96 | 24 | 0 | 0 | 5 | 0 | 18 | 1 | 0 | 0 |
| sqlglot | sqlglot_optimize_same_dialect | common_core_v0_40_same_engine_120 | 120 | 120 | 65 | 63 | 57 | 27 | 1 | 0 | 18 | 11 | 0 | 0 | 0 |
| sqlglot | sqlglot_transpile_same_dialect_noop | common_core_v0_40_same_engine_120 | 120 | 120 | 72 | 72 | 48 | 0 | 6 | 0 | 18 | 0 | 0 | 24 | 0 |
| calcite_hep | calcite_hep_fail_closed_120 | common_core_v0_40_same_engine_120 | 120 | 120 | 95 | 93 | 27 | 2 | 21 | 0 | 1 | 1 | 2 | 0 | 0 |
| r_bot | r_bot_same_engine_rewrite | common_core_v0_40_same_engine_120_and_pg_scoped_subsets | 120 | NA_not_retained | 15_pg_only_bounded | 15_pg_only_bounded | NA_not_retained | 2 | NA_not_retained | NA_not_retained | 80 | NA_not_retained | NA_not_retained | NA_not_retained | 0_on_pg15_bounded_timing_subset |
| llm_r2 | llm_r2_original_route_bounded_pg9 | common_core_v0_llm_r2_pg_supported_9 | 9 | 9 | 3_exact_plus_6_execution_failed | 3 | 6 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 3_exact_rows_without_retained_timing_packet |
| llm_r2 | llm_r2_recovered_extraction_route_v1 | common_core_v0_llm_r2_recovered_pg9_attempted_appendix | 9 | 9 | 6 | 6 | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 6_exact_rows_without_retained_timing_packet |
| learnedrewrite | UNKNOWN_NOT_RECOVERED | prior_method_pg10 | 10 | 10 | NA_not_retained | 10_checker_consistent_bounded | NA_not_auditable | 0 | NA_not_retained | NA_not_retained | NA_not_retained | 0 | 0 | 8 | NA_not_retained |

## Main patterns

- Main Track A routes retain explicit non-exact frontiers for Direct LLM, Direct LLM + Repair, SQLGlot optimize, SQLGlot no-op, and Calcite HEP.
- For Direct LLM + Repair-1, `executed=97` uses successful-execution semantics consistent with exact plus mismatch; the retained `115` value is only a ready-after-preflight / not-preflight-blocked count and is not used as executed.
- SQLGlot no-op keeps source-like/no-op rows visible rather than hiding them inside executed-subset exactness.
- SQLGlot optimize keeps generation/parse/execution/unsupported failures visible and retains the revised exact63 frontier.
- Bounded prior methods remain bounded and do not get forced into the 120-row denominator.
- LLM-R2 recovered remains a PG9 recovery audit row with a retained PG6 exact recovered subset; it is not restated as a standalone PG6 denominator row.

## Denominator cautions

- `common_core_v0_40_same_engine_120` applies only where the retained route actually uses the full Track A denominator.
- Bounded PG-only or mixed-scope appendix routes keep their own retained denominator ids and methodology boundaries.
- If a sub-bucket is not retained, it stays `NA_not_retained` rather than being inferred.

## Difference from hard-negative guardrail

- Hard-negative guardrail asks whether case-package known-negative controls were rejected.
- Candidate failure accounting asks how method-generated candidates populate exact, non-exact, and failure buckets.
- These answer different questions and must not be collapsed into one table.

## Safe prose snippet for the paper

Method candidate failures remain method behavior and must stay visible in the denominator-aware ledger. Generated-subset and executed-subset reporting can overstate apparent method quality, so exact rows, non-exact frontier rows, and retained failure buckets should be reported together. Hard-negative controls and method non-exact frontier accounting answer different questions and should remain in separate Section 8.6 tables.
