# Common-core v0 Fresh Controls @40 Execution Preflight

## Executive Summary

This is a fresh-execution preflight only. No databases were run, no SQL was executed, and no benchmark methods were launched.

The command matrix covers `360` rows for the frozen denominator: `40` cases x `3` engines x `3` control variants.

## Recommendation

Recommended order: run `source + human_positive` first, then run `hard_negative` separately.

Why:

- `native_source` and most `human_positive` routes have directly discoverable engine-specific commands and clearer expected artifacts.
- `hard_negative` currently reuses generic validation scripts rather than dedicated negative-only commands, so its semantics need explicit manual confirmation before execution.
- keeping `hard_negative` separate reduces the risk of mixing expected-failure semantics into the first denominator-complete fresh pass.
- `PORT_0003`, `PORT_0004`, and `PORT_0005` still lack dedicated human-positive commands in the preflight scan, which should remain explicit rather than patched over.

Running all controls together is not recommended for the first fresh pass because the negative route and the three PORT human-positive gaps need tighter operator review.

## Status Summary

- `ready_for_fresh_execution`: `223`
- `needs_manual_command_review`: `128`
- `skip_for_fresh_execution`: `9`

## Route Guidance

- `native_source`: use engine-specific validation scripts where present; these are the cleanest first-pass fresh controls rows.
- `human_positive`: use engine-specific plan-collection scripts where present; keep `PORT_0003`, `PORT_0004`, and `PORT_0005` skipped until a human approves the concrete command path.
- `hard_negative`: keep separate and operator-reviewed because current discoverable commands are generic validation scripts, not explicit negative-route launchers.

## Denominator Discipline

- The later fresh run must still preserve all `40` denominator cases.
- Missing, skipped, unsupported, or failed rows must remain visible in `run_event_long.csv`.
- `controls_summary.csv` must remain derived from `run_event_long.csv`.

## Environment Bootstrap

Use these environment entrypoints in the eventual execution shell:

```bash
source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh
```

## Validator Hook

After a real fresh run exists, validate with:

```bash
python scripts/common_core_v0_validation.py --manifest reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_manifest.json --run-event-long reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_event_long.csv --controls-summary reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/controls_summary.csv --json
```

## Boundary

This preflight does not authorize execution by itself. It only records the discoverable command surface and the recommended run ordering.
