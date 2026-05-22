# LLM-R2 Supported PG3 PostgreSQL Execution/Checker Review v1

This is governance review of a completed local human-run.

This packet is PG3-only.
It is not PG40 evidence.
It is not full `120` evidence.
It is not MySQL/Spark evidence.
It is not timing or speedup evidence.

## Scope Recap

Reviewed rows:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

Reviewed run:

- `reports/evaluation/common_core_v0/runs/llm_r2_supported_pg3_pg_execution_checker_02/`

Context note:

- `_01` failed at setup because PostgreSQL env was not loaded and `psql`
  attempted a local socket connection.
- `_02` succeeded after the project PostgreSQL env was loaded for the local
  human-run.

## Per-Row Result Table

| case_id | engine | setup_exit_code | source_exit_code | generated_exit_code | source_execution_status | generated_execution_status | exact_match | failure_bucket |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| `PERF_0006` | `pg` | `0` | `0` | `0` | `executed` | `executed` | `true` | `exact_match` |
| `PERF_0013` | `pg` | `0` | `0` | `0` | `executed` | `executed` | `true` | `exact_match` |
| `PERF_0024` | `pg` | `0` | `0` | `0` | `executed` | `executed` | `true` | `exact_match` |

## Artifact Table

| case_id | source_tsv_path | generated_tsv_path | result_check_path |
| --- | --- | --- | --- |
| `PERF_0006` | `workspaces/PERF_0006/pg/source.tsv` | `workspaces/PERF_0006/pg/generated.tsv` | `workspaces/PERF_0006/pg/result_check.json` |
| `PERF_0013` | `workspaces/PERF_0013/pg/source.tsv` | `workspaces/PERF_0013/pg/generated.tsv` | `workspaces/PERF_0013/pg/result_check.json` |
| `PERF_0024` | `workspaces/PERF_0024/pg/source.tsv` | `workspaces/PERF_0024/pg/generated.tsv` | `workspaces/PERF_0024/pg/result_check.json` |

## Exact-Match Summary

The retained `_02` run shows:

- `3 / 3` setup exit codes at `0`
- `3 / 3` source executions marked `executed`
- `3 / 3` generated executions marked `executed`
- `3 / 3` exact matches
- `3 / 3` failure buckets recorded as `exact_match`

The retained attestation also confirms:

- no timing
- no speedup
- no MySQL
- no Spark
- no PG40
- no full `120`
- no result card or proposed row

## Next Recommended Gate

Human decide whether to expand LLM-R2 from PG3 to a larger PostgreSQL slice, or
stop and report PG3 bounded evidence.

## Explicit Non-Claims

- This is governance review only.
- This does not create a result card or proposed row.
- This does not create a leaderboard.
- This does not claim PG40 evidence.
- This does not claim full `120` evidence.
- This does not claim MySQL/Spark evidence.
- This does not claim timing or speedup evidence.
- This does not update `method_comparison_summary_v2`.
