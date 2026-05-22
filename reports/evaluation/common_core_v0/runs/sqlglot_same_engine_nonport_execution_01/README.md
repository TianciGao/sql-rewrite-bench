# SQLGlot Non-PORT Same-Engine Execution

This package is human-run only. Codex must not execute the script in this directory.

Purpose:
- execute the broader non-PORT same-engine SQLGlot slice for Common-core v0
- cover `performance`, `consistency`, and `longtail`
- exclude all `PORT` cases
- preserve generation-failed and explicit no-op rows instead of silently dropping them

This package does not:
- run timing
- compute speedup
- compute regression metrics
- create a final leaderboard
- include `PORT`

Scope summary:
- cases: `31`
- rows: `186`
- ready-to-execute rows: `144`
- explicit generation-failed rows: `27`
- explicit no-op rows: `15`

Outputs expected after a human run:
- `run_results.json`
- `records.tmp.jsonl`
- `logs/*.log`
- `workspaces/...` for executed rows

Rows with `not_executed_generation_failed` and `noop_generated` should remain explicit in `run_results.json` even though they are not executed.

