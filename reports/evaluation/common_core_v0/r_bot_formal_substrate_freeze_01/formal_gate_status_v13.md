# Formal Gate Status v13

## Scope

This document updates the formal gate status after the successful human-run
artifact-contract validation for the formal `R-Bot` same-engine `120`-row
Common-core v0 package.

It incorporates:

- [formal_artifact_contract_validation_report.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_artifact_contract_01/formal_artifact_contract_validation_report.md)
- [formal_artifact_contract_validation_report.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_artifact_contract_01/formal_artifact_contract_validation_report.json)
- [runtime_lock_status_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_lock_status_v1.md)
- [formal_gate_status_v12.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v12.md)
- [formal_gate_status_v11.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v11.md)
- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [r_bot_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_run_plan_v1.json)
- [r_bot_common_core_v0_40_same_engine_candidate_matrix.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not create benchmark metrics.
It does not by itself constitute denominator-aware formal run evidence.

## Direct Answers

- ZIP provenance closed: `yes`
- corpus text checks closed: `yes`
- contamination-check pre-generation blocker closed: `yes`
- retrieval-config freeze closed for pre-generation: `yes`
- frozen `100`-slot rule-vector catalog closed: `yes`
- formal Chroma index blocker closed: `yes`
- runtime/dependency lock blocker closed: `yes`
- retained run-path artifact-contract validation blocker closed: `yes`
- `120`-row denominator frozen: `yes`
- `current_benchmark_gate_ready` for starting formal generation: `true`
- formal `R-Bot @120` generation package may be created and human-run: `yes`
- benchmark metrics already exist: `no`

## What v13 Closes

Closed by this update:

1. the retained run-path artifact-contract blocker is now closed
2. the formal pre-generation gate is now open for the denominator-aware `120`-row same-engine package
3. the frozen denominator and expected retained run-path layout are now validated together against the formal run plan
4. pre-generation governance dependencies are now simultaneously green:
   - retained ZIP provenance and corpus identity
   - retained corpus text extraction contract and row counts
   - retained retrieval-config freeze
   - retained rule-vector catalog freeze
   - retained formal Chroma index build and inspect
   - retained runtime/dependency lock
   - retained artifact-contract validation

## Denominator Status

The denominator is frozen for formal generation:

- `denominator_id = common_core_v0_40_same_engine_120`
- `case_count = 40`
- engines: `pg`, `mysql`, `spark`
- `planned_rows = 120`
- counts by engine: `40 / 40 / 40`

The passing artifact-contract validator confirms:

- `candidate_matrix_rows = 120`
- `contract_matrix_rows = 120`
- row-status coverage remains explicit for `generated`, `failed`, `blocked`, `unsupported`, and `skipped`

## Pre-Generation Decision Boundary

As of v13, the formal package is allowed to move from pre-generation freeze to
human-run formal generation setup.

This means:

- the formal `R-Bot @120` generation package may now be created and human-run
- `current_benchmark_gate_ready = true` for starting that formal generation package

This does not mean:

- benchmark metrics already exist
- leaderboard evidence exists
- speedup or timing claims are authorized
- denominator-aware formal run evidence has already been retained

## What Remains Downstream

The following remain downstream of v13 and will be produced only by the actual
formal `@120` generation, execution, and timing phases:

1. denominator-aware formal run artifacts under the planned run root
2. retained row-level generation outputs for all represented statuses
3. run-level evidence proving the formal package actually executed
4. any later execution, validation, timing, or metric artifacts

The contamination guard remains a run-artifact attestation requirement during
the actual formal run. What is closed in v13 is the pre-generation blocker on
moving forward to that human-run package, not the future attestation payload
itself.

## Gate Outcome

As of v13:

- formal Chroma index blocker: closed
- runtime/dependency lock blocker: closed
- retained artifact-contract validation blocker: closed
- final pre-generation formal gate: open

Therefore:

- `current_benchmark_gate_ready = true`
- formal `R-Bot @120` generation package may be created and human-run: `yes`
- denominator-aware formal run evidence already exists: `no`

## Bottom Line

v13 closes the final pre-generation blocker. The formal R-Bot same-engine
`120`-row package is now fully frozen and benchmark-ready to start the
human-run formal generation phase.

That is a start-of-generation authorization only. It does not mean R-Bot
benchmark metrics already exist, and it does not replace the downstream
generation, execution, validation, timing, or evidence-retention phases.
