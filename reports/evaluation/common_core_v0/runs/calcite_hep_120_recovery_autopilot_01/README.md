# Calcite HEP 120 Recovery Autopilot 01

This package is a bounded, fail-closed control packet for the retained Calcite
HEP recovery frontier after the ledger reached `90/120`.

It is human-run only. Codex must not execute it.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous fail-closed exact ledger: `90/120`
- planned rows: `0`
- maximum possible ledger after this autopilot: `90/120`

## Why Planned Rows Are Zero

The retained evidence no longer supports a bounded low-risk or medium-low-risk
autopilot batch:

- remaining executable mismatches are semantic or output-shape failures
- remaining non-executed rows are methodology-boundary `PORT` rows
- no retained row remains in a pure harness/rendering/setup state comparable to
  prior successful recovery packets

## Boundary

- recovery-autopilot validity evidence only
- no timing
- no speedup
- no leaderboard
- no full `120`-row comparable claim

## Intended Use

Run this package only if you want a retained no-op control artifact that:

- confirms the frontier is presently closed from a safe autopilot standpoint
- writes a fresh `run_results.json`
- writes a fresh `run_event_long.csv`
- preserves fail-closed accounting without silently broadening scope
