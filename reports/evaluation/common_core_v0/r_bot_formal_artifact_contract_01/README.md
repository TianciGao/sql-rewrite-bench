# R-Bot Formal Artifact Contract Package

This package freezes the pre-generation retained artifact-contract validation step for the formal `R-Bot` same-engine `120`-row Common-core v0 run.

It is human-run only.
It does not run `R-Bot`.
It does not call an LLM or provider API.

## Main Inputs

- `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_artifact_contract_v1.md`
- `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_run_plan_v1.json`
- `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv`
- `reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_lock_status_v1.md`
- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v12.md`

## Human-Run Entry Point

```bash
python reports/evaluation/common_core_v0/r_bot_formal_artifact_contract_01/run_manual_r_bot_formal_artifact_contract_validate.py
```

## Role of the Validator

The validator checks only contract completeness and schema/path definitions.

It validates:

- exact `120`-row denominator coverage
- deterministic row-level artifact paths
- required schema-key definitions
- row-status coverage for `generated`, `failed`, `blocked`, `unsupported`, and `skipped`
- structured secret-hygiene rules, then applies them only when scanning actual retained artifacts

It does not require generated outputs to exist already.

## Decision Boundary

A successful validator run closes the retained run-path artifact-contract blocker only.

Formal `R-Bot @120` generation may start only after:

- this validator passes
- prior substrate and runtime locks remain green

That still does not create benchmark evidence by itself.
