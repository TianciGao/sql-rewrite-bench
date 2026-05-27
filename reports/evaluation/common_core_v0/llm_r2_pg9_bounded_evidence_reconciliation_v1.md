# LLM-R2 PG9 Bounded Evidence Reconciliation v1

This is documentation and evidence reconciliation only.

No LLM-R2 inference, PostgreSQL, MySQL, Spark, checker, timing, speedup, or
benchmark command was run for this packet.

## Scope

This packet reconciles retained `llm_r2` bounded PostgreSQL-supported
Common-core evidence on 9 PG rows:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`

Boundary:

- PG rows only: `9`
- not PG40 evidence
- not MySQL/Spark evidence
- not tri-engine `120` evidence
- not timing evidence
- `leaderboard_comparable = no`
- paper placement: bounded PG-only appendix evidence

## Evidence Rollup

| method_id | route_or_scope | denominator_scope | case_count | generation_attempted_rows | generated_rows | source_executed_rows | generated_executed_rows | exact_match_rows | execution_failed_rows | timing_rows | leaderboard_comparable | paper_table_placement |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `llm_r2` | `bounded_pg_supported_common_core` | `common_core_v0_llm_r2_pg_supported_9` | `9` | `9` | `9` | `9` | `3` | `3` | `6` | `0` | `no` | `bounded_pg_only_appendix_evidence` |

## Per-Case Table

| case_id | engine | generated_status | source_execution_status | generated_execution_status | exact_match | failure_bucket | refined_failure_class | retained_run_artifact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | `not_applicable_exact_match` | `runs/llm_r2_supported_pg3_pg_execution_checker_02` | completed bounded PG3 exact-match evidence |
| `PERF_0008` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | `malformed_generated_sql_missing_leading_select_or_with` | `runs/llm_r2_common_core_pg6_pg_execution_checker_01` | generated SQL retained; PostgreSQL execution failed before result comparison |
| `PERF_0013` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | `not_applicable_exact_match` | `runs/llm_r2_supported_pg3_pg_execution_checker_02` | completed bounded PG3 exact-match evidence |
| `PERF_0017` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | `malformed_generated_sql_missing_leading_select_or_with` | `runs/llm_r2_common_core_pg6_pg_execution_checker_01` | generated SQL retained; PostgreSQL execution failed before result comparison |
| `PERF_0019` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | `malformed_generated_sql_missing_leading_select_or_with` | `runs/llm_r2_common_core_pg6_pg_execution_checker_01` | generated SQL retained; PostgreSQL execution failed before result comparison |
| `PERF_0024` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | `not_applicable_exact_match` | `runs/llm_r2_supported_pg3_pg_execution_checker_02` | completed bounded PG3 exact-match evidence |
| `PERF_0033` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | `malformed_generated_sql_missing_leading_select_or_with` | `runs/llm_r2_common_core_pg6_pg_execution_checker_01` | generated SQL retained; PostgreSQL execution failed before result comparison |
| `PERF_0052` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | `sql_syntax_error` | `runs/llm_r2_common_core_pg6_pg_execution_checker_01` | retained generated SQL appears malformed with truncated CTE/WITH structure |
| `PERF_0054` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | `malformed_generated_sql_missing_leading_select_or_with` | `runs/llm_r2_common_core_pg6_pg_execution_checker_01` | generated SQL retained; PostgreSQL execution failed before result comparison |

## Failure Taxonomy

- The PG3 rows `PERF_0006`, `PERF_0013`, and `PERF_0024` are retained bounded
  PG exact-match evidence.
- The PG6 rows all retained generated SQL and all retained source-side
  execution, but the generated SQL failed PostgreSQL execution.
- `PERF_0008`, `PERF_0017`, `PERF_0019`, `PERF_0033`, and `PERF_0054` are
  retained as `execution_failed` with refined failure class
  `malformed_generated_sql_missing_leading_select_or_with`.
- `PERF_0052` is retained as `execution_failed` with refined failure class
  `sql_syntax_error`; the retained generated SQL appears malformed with a
  truncated CTE/WITH-style structure.
- These 6 rows count as explicit `execution_failed` rows. They do not count as
  `mismatch`, and they do not count as `exact_match`.

## Paper-Safe Statement

`LLM-R2` has bounded PostgreSQL-supported Common-core evidence on 9 PG rows.
Retained evidence supports `9/9` generation attempts and `9/9` generated SQL
files. Retained evidence supports `3/9` generated SQL executions and `3/9`
exact matches. `6/9` generated SQL files failed PostgreSQL execution due to
malformed SQL. This is PG-only bounded evidence, not PG40, not tri-engine
`120`, not timing evidence, and not leaderboard-comparable.

## Non-Claims

- This does not create a leaderboard.
- This does not update `method_comparison_summary_v2`.
- This does not create a full `120`-row `LLM-R2` row.
- This does not claim MySQL/Spark support.
- This does not claim timing or speedup.
- This does not treat manually repairable SQL as method success.
- This does not authorize manual SQL repair as evidence.

## Next Action

- Stop `LLM-R2` full-`120` pursuit for now unless a separate
  wrapper/extraction-recovery task is explicitly approved.
- Preserve `LLM-R2` as bounded PG-only appendix evidence.
- Optional future work: keep any extraction-recovery audit separate from this
  original-output evidence packet.
