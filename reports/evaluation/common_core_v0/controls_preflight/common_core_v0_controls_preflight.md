# Common-core v0 Controls @40 Preflight

## Executive Summary

This is a dry-run controls preflight for the frozen Common-core v0 40-case denominator. No databases were run, no benchmark methods were executed, and no real `run_event_long` results were populated.

The scanned denominator contains `40` cases with pool mix `PERF=16`, `CONS=9`, `PORT=9`, `LONGTAIL=6`.

## Preflight Outcome

- `ready_for_controls_dry_run`: `40`
- `artifact_gap_review_needed`: `0`

All `40` cases have discoverable case directories, `source.sql`, positive rewrite, negative rewrite, and existing result / plan check artifacts in the current scanned layout.

## Command Discovery Notes

- Native/source execution commands were discovered from case-local `validation/` scripts for all scanned rows.
- Dedicated human-positive plan-collection commands were not discovered for `3` cases: `PORT_0003, PORT_0004, PORT_0005`.
- Where no dedicated human-positive command was discovered, the artifact map keeps the field blank and carries a caveat instead of inventing a command.

## Expected Engine Scope

- All denominator rows currently point to tri-engine expected scope from `inventory/case_registry.csv` via `validated_engines`.
- This preflight does not reinterpret those registry facts or authorize execution.

## Planned Outputs

- `common_core_v0_controls_artifact_map.csv`: per-case artifact and command map for Controls @40 planning
- `common_core_v0_controls_run_plan.json`: dry-run run manifest for later controls execution scaffolding

## Validator Hook

Future controls runs should validate with:

```bash
python scripts/common_core_v0_validation.py --manifest reports/evaluation/common_core_v0/controls_preflight/common_core_v0_controls_run_plan.json --run-event-long reports/evaluation/common_core_v0/run_event_long.csv --controls-summary reports/evaluation/common_core_v0/controls_summary.csv --json
```

## Boundary

This preflight does not populate real evaluation outputs and does not start Controls @40 execution.
