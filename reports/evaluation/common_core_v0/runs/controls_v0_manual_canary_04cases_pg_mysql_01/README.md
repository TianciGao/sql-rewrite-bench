# Controls v0 Manual Canary 04 Cases PG/MySQL 01

This package is for a human to run from the real repository root. Codex must not execute the script as part of this package creation step.

Scope:
- cases: `PERF_0006`, `CONS_0007`, `LONGTAIL_0011`, `PORT_0012`
- engines: `pg`, `mysql`
- validation only
- no Spark execution yet
- no plan collection yet
- no separate hard-negative command

What success means:
- the PG/MySQL validation scripts for representative Common-core v0 pools can run from the real repo root
- stdout/stderr logs and `run_results.json` are produced under this run directory
- any missing script is recorded explicitly as `missing_script` rather than silently skipped

What this is not:
- not a full `@40` controls run
- not a leaderboard run
- not `run_event_long` materialization
- not a Spark canary

Follow-on expectation:
- `run_event_long` materialization comes only after this manual canary succeeds and the human confirms the resulting case-local artifacts are trustworthy.

Usage:
```bash
cd /home/tianci_gao/code/sql-rewrite-bench
bash reports/evaluation/common_core_v0/runs/controls_v0_manual_canary_04cases_pg_mysql_01/run_manual_canary.sh
```

Warning:
- the validation scripts may regenerate files under `cases/.../runs/`
- the script does not `git add` anything
