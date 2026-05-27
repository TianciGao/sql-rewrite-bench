# LLM-R2 Supported PG3 PostgreSQL Execution Input Recovery v1

This is read-only path recovery only.

No PostgreSQL execution, checker, timing, or speedup was run.

## Recovery Summary

This packet recovers PostgreSQL execution/checker input paths for the retained
LLM-R2 PG3 generated SQL:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

Preferred path policy used here:

1. case-local canonical path under `cases/`
2. controls snapshot copy under
   `reports/evaluation/common_core_v0/runs/controls_v0_fresh_source_positive_01/tmp_repo/`
3. prior retained run workspace copy under `reports/evaluation/common_core_v0/runs/.../workspaces/`

The preferred path is the canonical case-local path whenever it exists and
matches the expected case package layout. Secondary copies are retained only as
provenance and ambiguity context.

## Per-Case Recovery Table

| case_id | generated_sql_path | source_sql_path | ddl_pg_path | pg_witness_data_path | source_recovery_status | ddl_recovery_status | witness_recovery_status | usable_for_future_execution_planning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0006/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0006/source.sql` | `cases/PERF/PERF_0006/schema/ddl_pg.sql` | `cases/PERF/PERF_0006/validation/pg_witness_data.sql` | `recovered` | `recovered` | `recovered` | `yes` |
| `PERF_0013` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0013/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0013/source.sql` | `cases/PERF/PERF_0013/schema/ddl_pg.sql` | `cases/PERF/PERF_0013/validation/pg_witness_data.sql` | `recovered` | `recovered` | `recovered` | `yes` |
| `PERF_0024` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0024/generated_sql_schema_native_clean_v2.sql` | `cases/PERF/PERF_0024/source.sql` | `cases/PERF/PERF_0024/schema/ddl_pg.sql` | `cases/PERF/PERF_0024/validation/pg_witness_data.sql` | `recovered` | `recovered` | `recovered` | `yes` |

## Ambiguity Notes

- All 3 cases also exist under the retained controls snapshot:
  - `reports/evaluation/common_core_v0/runs/controls_v0_fresh_source_positive_01/tmp_repo/cases/PERF/...`
- All 3 cases also have prior retained PG workspace copies from other methods
  and runs under `reports/evaluation/common_core_v0/runs/.../workspaces/...`
- Those alternate copies are plausible but are not preferred because the
  canonical case-local package already contains the required PostgreSQL source,
  DDL, and witness inputs.
- `PERF_0024` source provenance was previously unrecovered in the execution plan
  packet, but the case-local `source.sql` is now explicitly recoverable and is
  consistent with case-registry metadata pointing to TPC-H Query 20.

## Later Approval Readiness

PostgreSQL execution/checker can now be considered for later human approval on
an input-path basis only because:

- all 3 generated SQL paths are retained
- all 3 source SQL paths are recovered
- all 3 PostgreSQL DDL paths are recovered
- all 3 PostgreSQL witness-data paths are recovered

This packet does not authorize PostgreSQL execution or checker work.

## Explicit Non-Claims

- This is read-only path recovery only.
- No PostgreSQL execution was run.
- No checker was run.
- No timing or speedup was run.
- This does not claim correctness or exact match.
- This does not claim MySQL/Spark support.
- This does not claim `120`-row evidence.
- This does not create a result card, proposed row, or leaderboard.
