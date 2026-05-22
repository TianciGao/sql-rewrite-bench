# Expected Artifacts

Human-run script:

- [run_manual_sqlglot_execution_canary.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/sqlglot_same_engine_execution_canary_01/run_manual_sqlglot_execution_canary.sh)

Primary run-local outputs after a human executes it:

- `logs/env_check.stdout.log`
- `logs/env_check.stderr.log`
- `logs/<case>__<engine>__<route>.stdout.log`
- `logs/<case>__<engine>__<route>.stderr.log`
- `records.tmp.jsonl`
- `run_results.json`

Run-local staging workspaces:

- `workspaces/PERF_0006/<engine>/<route>/`
- `workspaces/CONS_0007/<engine>/<route>/`
- `workspaces/LONGTAIL_0011/<engine>/<route>/`

Expected staged files per workspace:

- copied source SQL
- copied generated SQL
- copied engine-specific DDL
- copied engine-specific witness data

Expected row semantics in `run_results.json`:

- `executed`
- `not_executed_generation_failed`
- `noop_generated`
- `script_error`

For the current chosen scope, all rows are currently expected to start as `ready_to_execute`.
