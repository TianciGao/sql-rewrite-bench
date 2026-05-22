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
  - `case_scope`
  - `engine_scope`
  - `route_scope`
  - `records`

Each explicit matrix row should remain visible through one of these states:
- `executed`
- `skipped_unsupported`
- `not_executed_generation_failed`
- `noop_generated`
- `script_error`

Executed rows may create workspace-local copied inputs under `workspaces/<case_id>/<engine>/<route_id>/`.
No timing or leaderboard artifacts should be produced in this package.

