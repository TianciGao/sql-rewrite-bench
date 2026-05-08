# R-Bot Formal Artifact-Contract Validation Plan

## Role

This package freezes a human-run, pre-generation validation step for the retained run-path artifact contract of the formal `R-Bot` same-engine Common-core v0 run.

It does not run `R-Bot`.
It does not call an LLM or provider API.
It does not require generated outputs to exist yet.

## Inputs

- `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_artifact_contract_v1.md`
- `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_run_plan_v1.json`
- `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv`
- `reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_lock_status_v1.md`
- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v12.md`
- `reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/recovery_generation_triage.md`
- `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`

## Purpose

The validator closes the retained run-path artifact-contract blocker only if the formal run package definition is complete and internally consistent before any `@120` generation is attempted.

It validates:

- denominator coverage for exactly `120` rows
- fixed path layout for all `40` cases x `3` engines
- required schema-key definitions for row-level and package-level artifacts
- representation of non-success rows without silent dropping
- structured secret-hygiene rules for retained artifacts
- compatibility with the already-frozen formal Chroma index and runtime lock

## Expected Formal Run Root

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/`

## Required Row-Level Artifacts

For every denominator row, the contract package freezes expected retained paths for:

1. generated SQL
2. selected rules
3. retrieval trace
4. prompt text
5. raw response
6. token / cost / provider metadata
7. environment snapshot
8. row-level run metadata

Rows that are `blocked`, `unsupported`, `failed`, or `skipped` must still remain explicit in `run_event_long.csv` and `row_run_metadata.json` even if generated SQL does not exist for that row.

## Required Package-Level Artifacts

- `run_results.json`
- `run_event_long.csv`
- `generation_summary.csv` as a retained summary artifact
- validator outputs:
  - `formal_artifact_contract_validation_report.md`
  - `formal_artifact_contract_validation_report.json`

## Validation Scope

The validator is intentionally pre-generation and schema-first.

It must:

- require complete path definitions for all `120` rows
- require schema-key definitions for every artifact type
- require row-status enums that preserve denominator awareness
- not require generated outputs to already exist
- optionally inspect already-present files under the planned run root when they exist
- derive forbidden secret-token scans from structured policy rather than literal example assignments in the contract spec
- fail if any inspected retained file exposes a likely secret

## Pass Condition

The contract package passes only if all of the following are true:

- the expected-path specification is complete
- the `120`-row matrix is complete and deterministic
- path templates agree with the frozen run plan
- non-success rows remain representable without row dropping
- required package and row schema definitions are present
- the contract package describes forbidden secret classes structurally rather than embedding literal assignment examples

## Decision Boundary

Successful validation of this package closes only the retained artifact-contract blocker.

It does not itself create denominator-aware formal run evidence.
It does not authorize timing, speedup, or leaderboard claims.
