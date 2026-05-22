# R-Bot PG1 Recovery Canary Plan

This package prepares a one-case PostgreSQL recovery canary for `R-Bot` on frozen Common-core input `PERF_0006`.

It is a recovery package only.
It does not create current metrics.
It does not reuse old bounded numeric results as current `common_core_v0_40` metrics.

## Scope

- `method_id = r_bot`
- `denominator_id = common_core_v0_40_pg40`
- `canary_denominator_id = common_core_v0_40_perf_pg1_r_bot_recovery_canary`
- `case_id = PERF_0006`
- `pool = performance`
- `engine = pg`
- `route_id = r_bot_pg_rewrite`
- planned rows: `1`

## Exact Repo-Local Scaffold Found

Repo-local bounded scaffold commands exist in [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py):

- `python -m scripts.cli formal-rbot-llm4rewrite-adapter-preflight --case PERF_0006`
- `python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-preflight --case PERF_0006`
- `python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006 --dry-run --fresh-run-name`
- `python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006 --fresh-run-name`

Interpretation:

- the first three commands are the current recovery path for proving the canary is runnable
- the fourth is the actual one-case candidate-generation path if all gates are satisfied
- this is a bounded single-case scaffold, not a PG40 batch-generation path

## Retrieval / Policy State

- retrieval stack: `partial_tmp_only`
- retrieval corpus: `partial_tmp_only`
- prompt/demo policy: `not frozen`
- contamination guard: `not available as a frozen current-denominator contract`

So the canary is not treated as unconditionally runnable even though the repo CLI path exists.

## Recovery Objective

The canary should answer:

1. can the repo-local scaffold still find the upstream substrate and `/tmp` assets?
2. can the dry-run surface a stable expected generated-SQL path?
3. if the human explicitly allows it and dependencies are present, can one candidate SQL file be captured and copied into this run package?

## Generation Boundary

If a later human-run succeeds, the generated candidate should be copied to:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql`

If prerequisites are missing:

- do not fake outputs
- preserve the row as blocked with structured reasons in `run_results.json`

## Recommended Interpretation

This package is a **recovery canary**, not a current baseline generation result.

Success here only justifies:

- stabilizing the one-case path
- then considering a tiny bounded PG canary

It does not justify jumping directly to PG40 generation.
