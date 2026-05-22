# Controls v0 Manual PG/MySQL 40 01

This package is for a human to run from the real repository root. Codex must not execute the script as part of this package creation step.

Scope:
- denominator: full frozen Common-core v0 `40` cases from `reports/curation/common_core_v0_final_denominator.csv`
- engines: `pg`, `mysql`
- validation only
- no Spark execution yet
- no plan collection yet
- no separate hard-negative command

What success means:
- the PG/MySQL validation scripts for all `40` frozen denominator cases can run from the real repo root
- stdout/stderr logs and `run_results.json` are produced under this run directory
- any missing validation script is recorded explicitly as `missing_script` rather than silently skipped

What this is not:
- not a full controls `@40` evaluation package yet
- not a leaderboard run
- not `run_event_long` materialization
- not a Spark-inclusive controls run
- not a plan-observability pass

Follow-on expectation:
- `run_event_long` materialization comes only after this manual script succeeds and the human confirms the resulting case-local artifacts are trustworthy.

Usage:
```bash
cd /home/tianci_gao/code/sql-rewrite-bench
bash reports/evaluation/common_core_v0/runs/controls_v0_manual_pg_mysql_40_01/run_manual_controls_pg_mysql_40.sh
```

Warning:
- the validation scripts may regenerate files under `cases/.../runs/`
- the script does not `git add` anything
