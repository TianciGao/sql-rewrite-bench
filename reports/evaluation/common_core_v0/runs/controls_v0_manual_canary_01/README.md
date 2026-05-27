# Controls v0 Manual Canary 01

This package is for a human to run from the real repository root. Codex must not execute the script as part of this package creation step.

Scope:
- case: `PERF_0006`
- engines: `pg`, `mysql`
- validation only
- no Spark execution yet
- no PORT cases yet
- no plan collection yet
- no separate hard-negative command

What success means:
- `bash cases/PERF/PERF_0006/validation/run_pg_validation.sh` can run from the real repo root
- `bash cases/PERF/PERF_0006/validation/run_mysql_validation.sh` can run from the real repo root
- stdout/stderr logs and `run_results.json` are produced under this run directory

What this is not:
- not a full `@40` controls run
- not a leaderboard run
- not `run_event_long` materialization
- not a Spark or PORT canary

Follow-on expectation:
- `run_event_long` materialization comes only after this manual canary succeeds and the human confirms the resulting case-local artifacts are trustworthy.

Usage:
```bash
cd /home/tianci_gao/code/sql-rewrite-bench
bash reports/evaluation/common_core_v0/runs/controls_v0_manual_canary_01/run_manual_canary.sh
```

Warning:
- the validation scripts may regenerate files under `cases/PERF/PERF_0006/runs/`
- the script does not `git add` anything
