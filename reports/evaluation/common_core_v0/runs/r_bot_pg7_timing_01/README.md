# R-Bot PG7 Timing Package

This package prepares the human-run PostgreSQL timing experiment for the seven R-Bot rows that passed execution/validity with `match_exact`.

Scope in this package:

- method: `r_bot`
- route: `r_bot_same_engine_rewrite`
- engine: `pg`
- generation denominator reference: `common_core_v0_40_same_engine_120`
- timing denominator: `generated_pg7_match_exact_only`
- execution target: exactly the `7` rows retained in the PG7 execution package as `match_exact`

This package does not execute timing by itself and does not create any leaderboard artifact.

Run from repo root:

```bash
bash reports/evaluation/common_core_v0/runs/r_bot_pg7_timing_01/run_manual_r_bot_pg7_timing.sh
```
