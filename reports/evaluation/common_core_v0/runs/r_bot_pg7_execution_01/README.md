# R-Bot PG7 Execution Package

This directory is the human-run PostgreSQL execution/validity package for the
`7` generated rows retained from the formal R-Bot same-engine `@120`
generation run.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- generation denominator:
  - `common_core_v0_40_same_engine_120`
- execution denominator:
  - `generated_pg7_only`
- planned execution rows:
  - `7`

## Human-Run Entry Point

```bash
bash reports/evaluation/common_core_v0/runs/r_bot_pg7_execution_01/run_manual_r_bot_pg7_execution.sh
```

## Boundary

This package produces execution/validity evidence only for the generated PG7
subset.

It does not:

- imply `120` execution rows
- compute timing
- compute speedup
- create a leaderboard

Blocked, failed, and unsupported generation rows remain explicit generation
outcomes outside this execution subset.
