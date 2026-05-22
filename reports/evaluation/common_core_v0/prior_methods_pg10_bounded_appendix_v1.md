# Prior-Method PG10 Bounded Appendix v1

This appendix packet records retained bounded prior-method evidence for
`LearnedRewrite` and `LLM-R2` only.

It is paper-facing appendix material, not a leaderboard, not a canonical method
table update, and not `common_core_v0_40_same_engine_120` evidence.

## Purpose And Boundary

- denominator_id for both rows is `prior_method_pg10`
- engine scope is `pg_only`
- this is bounded prior-method evidence only
- this is not tri-engine same-engine evidence
- this does not update `method_comparison_summary_v2`
- this does not promote either method into the main same-engine method evidence
  table

## Compact Evidence Table

| method_id | route_id | denominator_id | case_count | engine_scope | planned_rows | generated_or_ready_rows | executed_rows | checker_consistent_or_exact_rows | fail_closed_ledger | exact_or_checker_consistent_among_executed | timing_success_rows | timing_denominator_id | gm_speedup | regression_rate_20pct | leaderboard_comparable |
|---|---|---|---:|---|---:|---:|---:|---:|---|---|---:|---|---|---|---|
| `learnedrewrite` | `UNKNOWN_NOT_RECOVERED` | `prior_method_pg10` | `10` | `pg_only` | `10` | `10` | `10` | `10` | `10/10` | `10/10` | `2` | `UNKNOWN_NOT_RECOVERED` | `0.6295872209675301` | `UNKNOWN_NOT_RECOVERED` | `no` |
| `llm_r2` | `UNKNOWN_NOT_RECOVERED` | `prior_method_pg10` | `10` | `pg_only` | `10` | `9` | `9` | `9` | `9/10` | `9/9` | `9` | `UNKNOWN_NOT_RECOVERED` | `0.9592371433387649` | `UNKNOWN_NOT_RECOVERED` | `no` |

## LearnedRewrite

Retained bounded evidence:

- denominator_id: `prior_method_pg10`
- planned rows: `10`
- generated rows: `10`
- executed rows: `10`
- checker-consistent rows: `10`
- fail-closed bounded ledger: `10/10`
- timing-success rows: `2`
- GM speedup on the bounded PG-only witness-scale slice: `0.6295872209675301`

Why LearnedRewrite is not promoted:

- retained evidence is PG-only, not tri-engine
- bounded denominator is `prior_method_pg10`, not
  `common_core_v0_40_same_engine_120`
- `8/10` outputs were source-like / no-op candidates
- only `2` non-noop candidates entered the bounded PG-only timing slice
- current repo-local readiness artifacts do not recover a `120`-row route
  substrate
- no retained MySQL evidence
- no retained Spark evidence

Unrecovered or missing fields:

- `route_id = UNKNOWN_NOT_RECOVERED`
  because no retained paper-facing or scratch artifact defines a formal route id
- `timing_denominator_id = UNKNOWN_NOT_RECOVERED`
  because the retained PG-only speedup slice does not expose a frozen timing
  denominator label
- `regression_rate_20pct = UNKNOWN_NOT_RECOVERED`
  because the retained artifacts expose `regression_count@20 = 2`, not a frozen
  rate field
- `unsupported_rows = UNKNOWN_NOT_RECOVERED`
- `parse_failed_rows = UNKNOWN_NOT_RECOVERED`
- `methodology_boundary_rows = UNKNOWN_NOT_RECOVERED`

Paper-safe statement:

`LearnedRewrite currently has bounded PG-only evidence on prior_method_pg10, not common_core_v0_40_same_engine_120 evidence. Retained artifacts support 10/10 generated, 10/10 executed, and 10/10 checker-consistent cases on that bounded denominator, but 8/10 outputs were source-like/no-op and only 2 non-noop candidates entered the bounded PG-only witness-scale timing slice. The current repo-local readiness artifacts do not recover a runnable 120-row same-engine route, and there is no retained MySQL or Spark evidence.`

## LLM-R2

Retained bounded evidence:

- denominator_id: `prior_method_pg10`
- planned rows: `10`
- generated rows: `9`
- executed rows: `9`
- checker-consistent rows: `9`
- fail-closed bounded ledger: `9/10`
- timing-success rows: `9`
- GM speedup on the bounded PG-only witness-scale slice: `0.9592371433387649`

Why LLM-R2 is not promoted:

- retained evidence is PG-only, not tri-engine
- bounded denominator is `prior_method_pg10`, not
  `common_core_v0_40_same_engine_120`
- one retained logical-plan-stage failure remained in-denominator
- current repo-local readiness artifacts do not recover a `120`-row route
  substrate
- no retained MySQL evidence
- no retained Spark evidence

Unrecovered or missing fields:

- `route_id = UNKNOWN_NOT_RECOVERED`
  because no retained paper-facing or scratch artifact defines a formal route id
- `timing_denominator_id = UNKNOWN_NOT_RECOVERED`
  because the retained PG-only speedup slice does not expose a frozen timing
  denominator label
- `regression_rate_20pct = UNKNOWN_NOT_RECOVERED`
  because the retained artifacts expose `regression_count@20 = 1`, not a frozen
  rate field
- `noop_rows = UNKNOWN_NOT_RECOVERED`
  because retained scratch notes only say `not_observed`, not a numeric frozen
  row total
- `unsupported_rows = UNKNOWN_NOT_RECOVERED`
- `parse_failed_rows = UNKNOWN_NOT_RECOVERED`
- `methodology_boundary_rows = UNKNOWN_NOT_RECOVERED`

Paper-safe statement:

`LLM-R2 currently has bounded PG-only prior-method evidence on prior_method_pg10, not common_core_v0_40_same_engine_120 evidence. Retained artifacts support 9/10 generated, 9/10 executed, and 9/10 checker-consistent cases on that bounded denominator, with one logical-plan-stage failure remaining explicit in the fail-closed ledger. The current repo-local readiness artifacts do not recover a runnable 120-row same-engine route, and there is no retained MySQL or Spark evidence.`

## Explicit Non-Claims

- This appendix does not create a leaderboard.
- This appendix does not update `method_comparison_summary_v2`.
- This appendix does not promote either method into canonical status.
- This appendix does not create a same-engine `120`-row proposed row.
- This appendix does not claim tri-engine support.
- This appendix does not claim cross-dialect portability evidence.
- This appendix does not claim that bounded PG-only timing slices are
  full-denominator leaderboard scalars.

## Source Artifacts Used

- [prior_methods_common_core_v0_40_preflight.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_preflight/prior_methods_common_core_v0_40_preflight.md)
- [prior_methods_candidate_matrix.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_preflight/prior_methods_candidate_matrix.csv)
- [PRIOR_METHOD_EVIDENCE_SUMMARY_RBOT_LEARNEDREWRITE_LLMR2_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_EVIDENCE_SUMMARY_RBOT_LEARNEDREWRITE_LLMR2_v1.md)
- [PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md)
- [LLMR2_10CASE_SMOKE_ROLLUP_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md)
- [PRIOR_METHOD_SPEEDUP_LEARNEDREWRITE_BATCH_C_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_SPEEDUP_LEARNEDREWRITE_BATCH_C_v1.md)
- [PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_v1.md)
- [learnedrewrite_input_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/learnedrewrite_input_readiness_v0.json)
- [rbot_llmr2_retrieval_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json)
