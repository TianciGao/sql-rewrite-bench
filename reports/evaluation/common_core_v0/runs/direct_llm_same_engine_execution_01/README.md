# Direct LLM @40 Same-Engine Execution

This package is **human-run only**. Codex must not execute the script in this directory.

Purpose:

- prepare same-engine execution for the completed Direct LLM generation run
- cover all `40` Common-core v0 denominator cases
- keep all `120` case-engine rows explicit
- preserve blocked rows and caveated rows instead of silently dropping them

This package does not:

- call any LLM or API
- modify generated SQL outputs
- compute timing
- compute speedup
- create a leaderboard

Scope summary:

- planned rows: `120`
- ready_to_execute rows: `115`
- rows with preflight caveats: `22`
- blocked rows due to missing witness-data artifacts: `5`

Blocked rows are currently:

- `PORT_0003 / mysql`
- `PORT_0003 / spark`
- `PORT_0004 / pg`
- `PORT_0005 / mysql`
- `PORT_0005 / spark`

Key portability watchlist:

- `PORT_0013 / spark` from generation triage

Outputs expected after a human run:

- `run_results.json`
- `records.tmp.jsonl`
- `logs/*.log`
- `workspaces/.../source.tsv`
- `workspaces/.../generated.tsv`
- `workspaces/.../result_check.json`

No `run_event_long.csv`, timing outputs, speedup outputs, or leaderboard artifacts should be produced by this package.
