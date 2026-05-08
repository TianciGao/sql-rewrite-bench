# R-Bot Common-core v0 @40 Same-Engine Formal Protocol

## Role

This package defines the formal denominator-freeze and comparison-entry protocol for `R-Bot` on Common-core v0 same-engine evaluation.

It does not run databases.
It does not execute SQL.
It does not call any LLM/API.
It does not authorize benchmark execution by itself.

## Fixed Identity

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- case denominator source: `reports/curation/common_core_v0_final_denominator.csv`
- cases: all frozen `40` Common-core v0 cases
- engines: `pg`, `mysql`, `spark`
- planned rows: `120`

Formal `R-Bot` same-engine results, if they exist later, must be reported on this `120`-row denominator. The target is not `PG1`, `PG3`, or `PG40`.

## Recovery Boundary

The existing `PG1` packet remains recovery evidence only.

What `PG1` established:

- exploratory generation succeeded for `PERF_0006 / pg`
- retained generated SQL was copied into repo artifacts
- exploratory execution replay succeeded once
- `result_check_status = match_exact`

What `PG1` did **not** establish:

- current benchmark metric evidence
- timing readiness
- PG3 readiness
- PG40 readiness
- tri-engine same-denominator method readiness

Therefore:

- `PG1 exploratory success is recovery evidence only`
- it proves bounded feasibility
- it is **not** current Common-core benchmark metric evidence

## Denominator Rule

This protocol inherits the Common-core evaluation rule that denominator rows must remain explicit.

Therefore:

- all `120` rows stay visible in the candidate matrix and later raw tables
- unsupported rows must remain explicit
- failed rows must remain explicit
- blocked rows must remain explicit
- mismatched rows must remain explicit
- no silent dropping of `PORT`, `LONGTAIL`, `CONS`, or non-`pg` rows is allowed

`R-Bot` may enter same-denominator method comparison only as **coverage-aware evidence**.

## Historical Boundary

Old `R-Bot` `prior_method_pg10` values are historical-only.

They must not be reused as:

- current Common-core v0 same-engine coverage
- current Common-core v0 validity evidence
- current Common-core v0 timing evidence
- current Common-core v0 speedup evidence
- route-complete `r_bot_same_engine_rewrite` results

The formal route in this package starts fresh from the frozen `120`-row denominator.

## Formal Route Contract

Each planned row is:

- one `case_id`
- one target engine
- one route:
  `r_bot_same_engine_rewrite`

The route is same-engine only:

- `pg -> pg`
- `mysql -> mysql`
- `spark -> spark`

This package does not define:

- cross-engine translation
- portability transfer scoring
- merged method-family scoring

## Comparison Entry Rule

`R-Bot` may be compared against current same-denominator method packets only after it has:

1. denominator-complete planning on all `120` rows
2. a frozen substrate gate
3. a frozen parameter contract
4. an attested contamination guard
5. a satisfied retained-artifact contract
6. explicit raw result tables preserving blocked/failed/unsupported rows

Until then, `R-Bot` is protocol-defined but **not benchmark-ready**.

## Current Benchmark-Readiness State

Current state from the recovery package and gate documents:

- `current_benchmark_gate_ready = false`
- retrieval substrate is still `/tmp`-only
- retrieval corpus is still `/tmp`-only
- exact retrieval hyperparameters are not benchmark-frozen
- contamination guard is defined but not attested in run artifacts
- artifact contract is defined but not satisfied by a denominator-ready run
- rule-vector alignment still depends on exploratory patch behavior
- existing CLI scaffolds are single-case smoke oriented, not a formal `120`-row tri-engine runner

Accordingly:

- `engine_supported_by_current_runner = no`
- `runner_ready = no`
- `retrieval_substrate_ready = no`
- `demo_policy_frozen = no`
- `contamination_guard_attested = no`
- `artifact_contract_ready = no`

for all planned rows in the current candidate matrix.

## Parameter Policy

The formal parameter freeze for this route is recorded in:

- [r_bot_parameter_freeze_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v1.json)

Key fixed values:

- temperature: `0`
- top_p: `1`
- max_tokens: `2048` to align with the current Direct LLM same-engine generation run unless a documented method exception is approved later
- candidate_count: `1`
- feedback_rounds: `0`
- retry policy: infrastructure retry only; no semantic/manual fixes

Key currently blocked freeze items:

- exact retrieval `top_k`
- exact threshold / reranking configuration
- deterministic rule-vector alignment without exploratory patching

## Required Outputs For A Future Formal Run

If a future formal run is authorized, it must retain per-row and package-level artifacts under a formal `R-Bot` run root. The required retained outputs are frozen in:

- [r_bot_artifact_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_artifact_contract_v1.md)

## Current Comparison Claim Boundary

Current correct label:

`coverage_aware_same_denominator_planning_only_not_current_benchmark_metric_evidence`

No file in this package may claim:

- admitted Common-core evidence
- current same-engine leaderboard placement
- current `GM_Speedup`
- current `RegressionRate@20%`
- denominator-wide `R-Bot` success evidence

## Outputs

- candidate matrix:
  `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv`
- parameter freeze:
  `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v1.json`
- substrate freeze gate:
  `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_substrate_freeze_gate_v1.md`
- artifact contract:
  `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_artifact_contract_v1.md`
- run plan:
  `reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_run_plan_v1.json`

## Bottom Line

The formal target for `R-Bot` is a fresh `120`-row same-engine Common-core v0 denominator. `PG1` recovery proved bounded feasibility only. `R-Bot` can enter comparison only as coverage-aware evidence after the frozen substrate, parameter, contamination, artifact, and runner gates are all deliberately closed.
