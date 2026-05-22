# SQLGlot Same-Engine @40 Preflight

This preflight defines the Common-core v0 same-engine SQLGlot evaluation packet without executing SQLGlot.

## Scope

- denominator: `common_core_v0_40`
- attempted cases: `40`
- planned routes:
  - `sqlglot_optimize_same_dialect`
  - `sqlglot_transpile_same_dialect_noop`
- planned engines: `pg`, `mysql`, `spark`
- output root: `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_01/`

## Readiness Basis

The readiness basis is the denominator-complete controls package in `common_core_v0_controls_status_table_v2.csv`.
That package shows:

- fresh manual validation rows for all non-unsupported controls combinations
- explicit `skipped_unsupported` rows for unsupported PORT native-source combinations
- no missing denominator rows

This supports a denominator-first SQLGlot preflight, but it does not by itself make SQLGlot a ready leaderboard result.

## Preflight Status Counts

- `ready_for_same_engine_sqlglot_preflight`: 29
- `ready_with_human_review_caveat`: 2
- `needs_port_route_review`: 9

## Interpretation

### Ready without extra route review

These cases have tri-engine fresh controls evidence and no portability-native-source exception in the controls package:

- performance cases except `JOB/IMDB` interpretation caveat rows
- consistency cases
- longtail cases

### Ready with human review caveat

- `PERF_0077`
- `PERF_0082`

These are bounded `JOB/IMDB` real-schema bridge cases. They can stay in the SQLGlot same-engine denominator plan, but downstream leaderboard interpretation still needs the existing human-gate framing.

### Needs PORT route review

All `PORT` cases remain in scope for denominator accounting, but same-engine SQLGlot route readiness is not uniform across engines.
Controls show that PORT native-source support is often fresh on only one engine, while other engine/route combinations remain explicit `skipped_unsupported` rows.

That means the SQLGlot run plan should keep PORT cases in the denominator, but it must preserve unsupported same-engine rows explicitly rather than silently dropping them.

## Output Plan

The planned SQLGlot run should write:

- `run_manifest.json`
- `run_event_long.csv`
- `method_case_summary.csv`
- `same_engine_leaderboard.csv`
- `validation_report.json`
- generated SQL artifacts under `generated/<case_id>/<engine>/<route_id>.sql`

## Validator

After materialization, validate with:

```bash
python scripts/common_core_v0_validation.py   --manifest reports/evaluation/common_core_v0/runs/sqlglot_same_engine_01/run_manifest.json   --run-event-long reports/evaluation/common_core_v0/runs/sqlglot_same_engine_01/run_event_long.csv   --method-case-summary reports/evaluation/common_core_v0/runs/sqlglot_same_engine_01/method_case_summary.csv   --same-engine-leaderboard reports/evaluation/common_core_v0/runs/sqlglot_same_engine_01/same_engine_leaderboard.csv   --json > reports/evaluation/common_core_v0/runs/sqlglot_same_engine_01/validation_report.json
```

## Boundary

This is a preflight only.
It does not execute SQLGlot, does not populate method results, and does not establish leaderboard readiness for performance metrics.
