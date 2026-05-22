# Autopilot Next Action

## Current State

The Calcite HEP fail-closed exact-match ledger currently stands at `90/120`.
The retained frontier is closed for safe implementation-level autopilot
recovery from existing evidence.

## Why This Autopilot Plans Zero Rows

- remaining `PERF_0006:*` gaps are semantic mismatches
- remaining `PERF_0035:*` gaps are output-shape mismatches
- remaining `PORT_*` gaps are methodology-boundary parse/rewrite/execution
  limits

## Exact Next Local Command

```bash
bash reports/evaluation/common_core_v0/runs/calcite_hep_120_recovery_autopilot_01/run_manual_calcite_hep_120_recovery_autopilot_01.sh
```

## What That Command Does

- writes a retained `run_results.json`
- writes a retained `run_event_long.csv`
- confirms that the current autopilot frontier is closed at `90/120`
- does not claim timing, speedup, leaderboard, or full `120`-row comparability

## What Should Happen Next After That

If additional recovery is desired after this control packet, the next step is a
new methodology review rather than a broader autopilot retry.
