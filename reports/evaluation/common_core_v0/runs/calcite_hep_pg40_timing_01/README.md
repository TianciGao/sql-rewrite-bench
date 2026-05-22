# Calcite HEP PG40 Timing Package

This package prepares the human-run PostgreSQL timing experiment for Calcite HEP on the frozen `common_core_v0_40_pg40` denominator.

Scope in this package:

- method: `calcite_hep`
- route: `calcite_hep_pg_rewrite`
- engine: `pg`
- execution target: exactly the `21` timing-eligible `match_exact` rows from the PG40 validity phase

This package does not execute timing by itself and does not compute final `GM_Speedup`, final `RegressionRate@20%`, or any leaderboard artifact.

Run from repo root:

```bash
bash reports/evaluation/common_core_v0/runs/calcite_hep_pg40_timing_01/run_manual_calcite_hep_pg40_timing.sh
```
