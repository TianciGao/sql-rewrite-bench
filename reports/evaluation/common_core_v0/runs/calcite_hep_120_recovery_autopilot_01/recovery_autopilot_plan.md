# Recovery Autopilot Plan

## Purpose

Provide a bounded, repeatable control packet for the Calcite HEP fail-closed
recovery frontier after the retained ledger reached `90/120`.

## Current Ledger

- denominator_id: `common_core_v0_40_same_engine_120`
- previous_fail_closed_exact_ledger: `90/120`
- maximum_possible_ledger_after_this_autopilot: `90/120`

## Batch Policy

- prefer one bounded batch of at most `10` rows
- include only retained-evidence-based low-risk or medium-low-risk candidates
- if no safe candidates remain, keep the batch empty and write an explicit
  control artifact instead of improvising new recovery policy

## Autopilot Decision

Current retained evidence supports `0` safe rows for a new autopilot batch.

Excluded categories:

- semantic mismatch rows:
  - `PERF_0006:mysql`
  - `PERF_0006:spark`
- output-shape mismatch rows:
  - `PERF_0035:pg`
  - `PERF_0035:mysql`
  - `PERF_0035:spark`
- methodology-boundary `PORT` rows:
  - all remaining `PORT_*` gaps in the current gap matrix

## Success Rule

Because this packet intentionally plans `0` rows, the only valid outcomes are:

- `recovered_exact_count = 0`
- `new_fail_closed_exact_ledger = 90/120`

Any future row addition requires a new retained-evidence audit, not silent
expansion of this package.
