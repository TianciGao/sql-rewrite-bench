# Common-core v0 Controls @40 Execution Plan

## Scope

This document defines how a later Controls @40 run should be organized for the frozen Common-core v0 denominator.

It does not run databases.
It does not execute validation scripts.
It does not populate real `run_event_long` rows.

## Run Directory Convention

Each real Controls @40 run should use:

`reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/`

Recommended examples:

- `reports/evaluation/common_core_v0/runs/controls_20260507T120000Z/`
- `reports/evaluation/common_core_v0/runs/controls_v0_dryrun_01/`

Inside that run directory, the planned artifact paths are:

- run manifest:
  `reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_manifest.json`
- raw canonical event table:
  `reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_event_long.csv`
- derived controls summary:
  `reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/controls_summary.csv`
- validator output:
  `reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/validation_report.json`

## Denominator and Accounting

The run must bind to:

- `denominator_id = common_core_v0_40`
- denominator source:
  `reports/curation/common_core_v0_final_denominator.csv`

All `40` denominator cases must remain represented in reporting.

No failed case can be dropped.
No unsupported case can be dropped.
No timed-out case can be dropped.

If a control variant is not runnable for a specific case, that condition must still appear in `run_event_long.csv` as an explicit event row with failure or skip semantics rather than disappearing from the denominator.

## Control Variants

Each denominator case may emit up to three control variants:

1. `native/source`
2. `human_positive`
3. `hard_negative`

Recommended encoding in `run_event_long.csv`:

- `task_track = control`
- `route_id = native_source` for native/source
- `route_id = human_positive` for human_positive
- `route_id = hard_negative` for hard_negative

Recommended `rewrite_role` values:

- `source` for native/source
- `positive` for human_positive
- `negative` for hard_negative

Recommended `rewrite_id` values:

- `source` for native/source
- `rewrite_pos_01` for human_positive
- `rewrite_neg_01` for hard_negative

## Missing Dedicated Commands

The controls preflight artifact map identified no dedicated `human positive execution command` for:

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`

These rows must remain explicit in the run output without inventing commands.

Recommended representation:

- keep `route_id = human_positive`
- set `status = skipped` or `status = unsupported` depending on the operator decision
- set `failure_bucket = unsupported` or another explicit non-success bucket
- set `notes` to explain that no dedicated command was discovered in preflight
- set `speedup_exclusion_reason` because this row is not speedup-eligible

This preserves denominator visibility and avoids fabricating execution procedures.

## Negative Availability and Rejection

The preflight map already records `negative_available`.

Execution-time guidance:

- when `negative_available = yes`, the run may create a `hard_negative` event row
- when a negative control is executed and correctly rejected or fails as expected, record:
  - `negative_available = yes`
  - `negative_rejected = yes`
  - `status = success` if the expected rejection behavior is the success condition for the control policy, or use explicit control-oriented notes if the local reporting convention treats the rejection as a checked failure
- when the negative exists but cannot be executed, record:
  - `negative_available = yes`
  - `negative_rejected = no`
  - explicit `status`, `failure_bucket`, and `speedup_exclusion_reason`

Recommended additional raw-row field usage in practice:

- `notes` should explain whether the negative was expected to fail, was rejected by the engine, or was skipped

## Reuse Versus Fresh Execution

Controls runs may rely on two evidence modes:

1. reuse of existing `result_check.json` and `plan_check.json`
2. fresh execution and fresh plan/result collection

Recommended raw-row representation:

- `execution_phase = aggregate` or `verify_result` when reusing existing artifacts
- `execution_phase = execute` or `collect_plan` when fresh execution artifacts are created later
- `artifact_path` should point to the reused artifact path when reuse occurs
- `notes` should explicitly say `reused_result_check`, `reused_plan_check`, `fresh_result_check`, or `fresh_plan_check`
- `plan_artifact_status` should still be set consistently:
  - `present`
  - `missing`
  - `not_applicable`

The run should not blur reused evidence and fresh evidence into the same uninterpretable status.

## Engine Scope

The frozen denominator expects tri-engine scope across:

- `pg`
- `mysql`
- `spark`

Recommended raw-row encoding:

- use one raw event row per `case_id x control_variant x engine`
- populate:
  - `engine_target = postgresql` for `pg`
  - `engine_target = mysql`
  - `engine_target = spark`

If a later runner adds a canonical `engine` column, it should mirror the same engine identity and remain compatible with the validator.

## Canonical Raw Table

`run_event_long.csv` is canonical.

It must capture:

- successes
- failures
- skips
- unsupported rows
- reused artifact checks
- fresh execution checks

`controls_summary.csv` is derived from `run_event_long.csv`.

The summary must not invent denominator counts that cannot be traced back to raw rows.

## Planned Minimal Workflow

1. create the run directory under `reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/`
2. write `run_manifest.json`
3. materialize `run_event_long.csv` rows for all attempted controls evidence
4. derive `controls_summary.csv` from the raw rows
5. run the validator and write `validation_report.json`

## Validator Command

After outputs exist, validate with:

```bash
python scripts/common_core_v0_validation.py \
  --manifest reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_manifest.json \
  --run-event-long reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_event_long.csv \
  --controls-summary reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/controls_summary.csv \
  --json
```

Recommended shell redirection when a human actually runs it later:

```bash
python scripts/common_core_v0_validation.py \
  --manifest reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_manifest.json \
  --run-event-long reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/run_event_long.csv \
  --controls-summary reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/controls_summary.csv \
  --json \
  > reports/evaluation/common_core_v0/runs/controls_<timestamp_or_version>/validation_report.json
```

## Bottom Line

Controls @40 execution must remain denominator-first, raw-table-first, and explicit about missing or skipped control variants.

No failed case can be dropped, and `controls_summary.csv` must always be derived from `run_event_long.csv`.
