# Common-core v0 Controls @40 Expected Outputs

## Scope

This document defines the minimal columns and row semantics for the Controls @40 execution outputs.

It does not create real outputs.

## 1. controls run_manifest.json

Minimal required fields:

- `run_id`
- `method_id`
- `method_role`
- `is_leaderboard_method`
- `git_commit`
- `denominator_id`
- `attempted_cases`
- `artifact_paths`

Expected values for Controls @40:

- `method_id = controls`
- `method_role = controls`
- `is_leaderboard_method = false`
- `denominator_id = common_core_v0_40`
- `attempted_cases = 40`

Expected row semantics:

- one manifest per run directory
- describes the run-wide contract, not per-case outcomes
- may supply run-wide `git_commit` and `denominator_id` for validator backfill
- must not contain `admitted_common_core`

## 2. run_event_long.csv

Minimal required columns for Controls @40:

- `run_id`
- `event_id`
- `method_id`
- `method_version`
- `case_id`
- `pool`
- `source_family`
- `task_track`
- `engine_target`
- `rewrite_id`
- `rewrite_role`
- `attempt_index`
- `execution_phase`
- `status`
- `is_denominator_case`
- `is_valid_result`
- `is_speedup_eligible`
- `speedup_exclusion_reason`
- `result_match_status`
- `plan_artifact_status`
- `notes`

Recommended controls-specific columns to add when the real runner writes data:

- `route_id`
- `engine`
- `git_commit`
- `denominator_id`
- `negative_available`
- `negative_rejected`
- `artifact_reuse_mode`

Expected row semantics:

- canonical raw table for all controls evidence
- one row per observable event
- recommended granularity:
  `case_id x control_variant x engine`
- `task_track` should stay `control`
- `route_id` should distinguish:
  - `native_source`
  - `human_positive`
  - `hard_negative`
- missing command situations must be represented as explicit `skipped` or `unsupported` rows
- failed rows must remain present
- `speedup_ratio` must be absent unless `is_speedup_eligible = true`
- invalid or ineligible rows must carry `speedup_exclusion_reason`

## 3. controls_summary.csv

Minimal required columns:

- `run_id`
- `method_id`
- `control_group`
- `pool_scope`
- `denominator_cases`
- `control_events`
- `control_valid_cases`
- `control_failure_cases`
- `control_expected_behavior`
- `control_observed_behavior`
- `notes`

Recommended additional columns for the real derived output:

- `engine_scope`
- `distinct_case_count_seen`
- `skipped_cases`
- `unsupported_cases`
- `artifact_reuse_cases`

Expected row semantics:

- derived from `run_event_long.csv`
- not a raw evidence table
- denominator-aware counts must stay explicit
- failed, skipped, timed-out, and unsupported cases must remain represented through the denominator counts
- should allow separate rows for:
  - `native_source`
  - `human_positive`
  - `hard_negative`
  - pool slices such as `all`, `performance`, `consistency`, `portability`, `longtail`

## 4. validation output JSON

Minimal expected top-level fields:

- `ok`
- `denominator_id_expected`
- `denominator_case_count`
- `artifacts_checked`
- `issue_count`
- `issues`

Expected row semantics:

- one validation JSON per executed controls run
- produced by `scripts/common_core_v0_validation.py`
- records schema, denominator, and governance validation outcomes
- `issues` must remain explicit; no silent pass-through for malformed outputs

## Semantics Summary

- `run_manifest.json` defines the run-wide contract
- `run_event_long.csv` is the canonical raw table
- `controls_summary.csv` is derived from `run_event_long.csv`
- `validation_report.json` records validator output after files exist

No failed case may be dropped from denominator-aware reporting.
