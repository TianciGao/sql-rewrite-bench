# LLM-R2 Slice-to-Runner Compatibility Addendum v1

This is a compatibility addendum only, not a run.

No LLM-R2 execution was performed in this task.
No PostgreSQL, MySQL, Spark, checker, timing, or speedup work was performed in
this task.

## Purpose

The original bounded PostgreSQL overlap approval covered an 8-row PG slice.
A later read-only runner discovery audit found that the currently recovered
repo-local LLM-R2 runner declarations do not support all 8 approved rows.

Therefore, the original 8-row approval must not be executed as-is.

## Current Compatibility Result

Currently supported by recovered repo-local runner declarations for the
approved slice:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

Currently not supported by recovered repo-local runner declarations for the
approved slice:

- `PERF_0007:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `LONGTAIL_0011:pg`
- `LONGTAIL_0013:pg`

## Implication

- the original 8-row approval is superseded by this compatibility addendum
- the currently supported subset is a 3-row PostgreSQL slice
- the remaining 5 PostgreSQL rows require wrapper-extension planning before any
  later run discussion

## Boundary

- no MySQL or Spark support is recovered
- no database execution is authorized
- no checker is authorized
- no timing is authorized
- no result card or proposed row is authorized
- this addendum does not create `120`-row LLM-R2 evidence

## Source Basis

- current approved 8-row slice:
  - [llm_r2_bounded_pg_overlap_candidate_slice_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_candidate_slice_v1.csv)
- current approval boundary:
  - [llm_r2_bounded_pg_overlap_human_run_approval_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_human_run_approval_v1.md)
  - [llm_r2_bounded_pg_overlap_approval_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_approval_gate_v1.md)
- recovered runner declarations:
  - [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:240)
  - [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:48944)
- retained bounded historical runner evidence:
  - [LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_PERF_0006_v1.md)
  - [LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_SCHEMA_NATIVE_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_SCHEMA_NATIVE_PERF_0006_v1.md)
