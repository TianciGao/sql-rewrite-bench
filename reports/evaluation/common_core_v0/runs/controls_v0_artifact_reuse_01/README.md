# Controls v0 Artifact Reuse 01

## Scope

This run materializes a Common-core v0 Controls @40 artifact-reuse package only. No databases were run and no SQL was executed.

## Run Facts

- `run_id`: `controls_v0_artifact_reuse_01`
- `denominator_id`: `common_core_v0_40`
- `method_id`: `controls`
- `method_role`: `controls`
- `is_leaderboard_method`: `false`
- `attempted_cases`: `40`
- raw rows: `360`

## Artifact Reuse Policy

- `run_event_long.csv` is canonical and includes all 40 denominator cases.
- This run reuses case-local `result_check.json` and `plan_check.json` artifacts where present.
- `controls_summary.csv` is derived from `run_event_long.csv`.

## Control Variants

- `native_source` rows are recorded as artifact-reuse successes when case-local checks are present.
- `human_positive` rows are recorded as artifact-reuse successes when rewrite-positive files and reusable checks are present.
- `hard_negative` rows remain visible but are recorded as `skipped` placeholders because this artifact-reuse pass does not infer variant-specific negative rejection from case-level checks alone.

## PORT Caveat

- `PORT_0003`, `PORT_0004`, and `PORT_0005` keep the missing dedicated human-positive command caveat in `run_event_long.csv` notes.
- No commands were invented for those cases.

## Validation

The validator output is stored in `validation_report.json`.
If validation is not clean, issues must remain explicit rather than hidden.
