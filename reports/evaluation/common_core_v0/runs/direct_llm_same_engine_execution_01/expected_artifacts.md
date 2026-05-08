# Expected Artifacts

The human-run script should produce:

- `logs/env_check.stdout.log`
- `logs/env_check.stderr.log`
- one `stdout` and one `stderr` log per executed matrix row
- `records.tmp.jsonl` with one JSON record per env-check or matrix row
- `run_results.json` summarizing:
  - `run_id`
  - `mode`
  - `repo_root`
  - `denominator_id`
  - `method_id`
  - `route_id`
  - `planned_rows`
  - `ready_to_execute_rows`
  - `preflight_caveat_rows`
  - `blocked_rows`
  - `summary_counts`
  - `counts_by_pool`
  - `counts_by_engine`
  - `records`

Executed rows may create workspace-local copied inputs and outputs under:

- `workspaces/<case_id>/<engine>/<route_id>/source.sql`
- `workspaces/<case_id>/<engine>/<route_id>/generated.sql`
- `workspaces/<case_id>/<engine>/<route_id>/source.tsv`
- `workspaces/<case_id>/<engine>/<route_id>/generated.tsv`
- `workspaces/<case_id>/<engine>/<route_id>/result_check.json`

Expected row semantics in `run_results.json`:

- `ready_to_execute` rows remain explicit whether they match or fail
- blocked rows remain explicit as `not_executed_preflight_blocked`
- consistency mismatches remain explicit as `mismatch`
- no timing, speedup, or leaderboard artifacts are produced
