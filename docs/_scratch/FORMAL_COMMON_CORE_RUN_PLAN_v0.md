# FORMAL_COMMON_CORE_RUN_PLAN_v0

## 1. Status

This is a tracked scratch formal common-core run plan.

This document defines how to upgrade the completed baseline smoke routes into a paper-facing formal common-core experiment run.

This document is a planning document only.

This document is not:

- an experiment result
- a registry writeback
- a common-core admission decision
- a leaderboard definition
- correctness scoring
- speedup scoring
- a formal review update
- a benchmark protocol freeze

## 2. Inputs And References

Primary tracked references:

- `docs/_scratch/BASELINE_ROUTE_READINESS_CLOSEOUT_v0.md`
- `docs/_scratch/PAPER_EXPERIMENT_DENOMINATOR_FREEZE_PLAN_v0.md`
- `docs/_scratch/PORT_0012_FAILURE_ANALYSIS_PACKET_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `docs/_scratch/BASELINE_SMOKE_READINESS_ROLLUP_v0.md`

Relevant existing smoke-report references if needed during later execution planning:

- PG control smoke summaries for Step 1
- SQLGlot same-dialect smoke summaries for Step 2a
- Direct LLM rewrite smoke summaries for Step 4a
- prompt package and token-usage artifacts associated with Step 4a

Planning assumption:

- the formal common-core denominator below is still a proposal for formal execution
- it is not a registry admission action

## 3. Formal Common-Core Denominator

Proposed first formal common-core denominator:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

| case_id | pool | source family | role in formal common-core | current smoke evidence | caveat |
|---|---|---|---|---|---|
| `PERF_0006` | `performance` | `TPC-H` | clean PG-native performance witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | formal denominator is still proposed, not admitted |
| `PERF_0008` | `performance` | `TPC-H` | clean PG-native performance witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | formal denominator is still proposed, not admitted |
| `PERF_0013` | `performance` | `TPC-H` | interval/date-bearing PG-native performance witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | repeated runtime and timeout policy are not yet frozen |
| `PERF_0017` | `performance` | `TPC-H` | interval/date-bearing PG-native performance witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | repeated runtime and timeout policy are not yet frozen |
| `PERF_0024` | `performance` | `TPC-H` | correlated-subquery PG-native performance witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | formal correctness wiring still needs confirmation |
| `PERF_0033` | `performance` | `TPC-DS` | clean PG-native TPC-DS witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | plan normalization expectations are not yet frozen |
| `PERF_0054` | `performance` | `TPC-DS` | clean PG-native TPC-DS witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | plan normalization expectations are not yet frozen |
| `CONS_0007` | `consistency` | `Calcite` | semantic stress consistency witness | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | semantic-support lines remain separate from this formal run |
| `CONS_0012` | `consistency` | `Calcite` | semantic stress consistency witness with threshold behavior | included in completed PG-native smoke controls, SQLGlot same-dialect, and Direct LLM rewrite | semantic-support lines remain separate from this formal run |

## 4. Included Formal Routes

| route | baseline_id | current smoke status | formal-run role | expected outputs | claim boundary |
|---|---|---|---|---|---|
| `NATIVE_IDENTITY` | `NATIVE_IDENTITY` | completed PG-native smoke | source control route | per-case control records, runtime records, consistency summaries, plan artifacts, route JSON | control evidence only, not leaderboard result by itself |
| `HUMAN_REFERENCE_POSITIVE` | `HUMAN_REFERENCE_POSITIVE` | completed PG-native smoke | positive rewrite control route | per-case execution records, runtime records, consistency summaries, plan artifacts, route JSON | execution and comparison evidence only |
| `HARD_NEGATIVE_GUARD` | `HARD_NEGATIVE_GUARD` | completed PG-native smoke | negative rejection control route | negative-guard summaries, rejection records, failure-category summaries, route JSON | guard behavior evidence only |
| `SQLGLOT_OPT_SAME_DIALECT` | `SQLGLOT_OPT_SAME_DIALECT` | completed PG-native smoke | deterministic same-dialect rewrite baseline | per-case rewrite records, consistency summaries, runtime and speedup summaries, plan summaries, route JSON | not semantic equivalence or speedup claim until formal gating is applied |
| `LLM_DIRECT_REWRITE_STRONG` | `LLM_DIRECT_REWRITE_STRONG` | completed PG-native smoke | paper-facing learned rewrite baseline | prompt metadata, token summaries, extracted SQL records, execution/consistency summaries, runtime summaries, plan summaries, route JSON | not correctness or speedup claim until formal gating is applied |

## 5. Excluded / Separate Routes

The following routes are intentionally excluded from the first formal common-core run:

- `SQLGlot transpile` and `LLM translate` are PORT-route lines, not PG-native common-core lines.
- `Calcite HEP`, `LearnedRewrite`, `GenRewrite`, and `R-Bot / LLM-R2` are readiness-only or deferred scaffold lines and are not runnable formal common-core baselines.
- `SlabCity` is deferred and lacks a runnable local adapter or reproducible service contract.
- `SQLSolver / VeriEQL` are support-only verifier lines and are not main leaderboard or speedup routes.

This keeps the first formal common-core run constrained to routes that already have completed PG-native smoke evidence.

## 6. Required Metrics

### 6.1 Correctness Metrics

- `ExecutableRate`
- `ResultConsistencyRate`
- executable-vs-consistency gap
- `NegativeRejectionRate`
- `FalseAcceptRate` if the hard-negative checker supports it
- failure count by route
- failure category by route

### 6.2 Performance Metrics

- `runtime_ms` per case and route
- source runtime vs rewrite runtime where applicable
- `GM_Speedup` for valid rewrites only
- `Win / Tie / Loss`
- `RegressionRate@20%`
- timeout count if applicable

### 6.3 Plan Observability Metrics

- plan artifact availability
- `PlanParseRate`
- source / rewrite plan pair availability
- operator delta availability
- `NodeAlignmentCoverage` if implemented
- `AttributionCoverage` if implemented
- unattributed speedup / regression count

### 6.4 LLM Cost Metrics

- `model_label`
- `provider_mode`
- `prompt_hash`
- `token_usage_input`
- `token_usage_output`
- `token_usage_total`
- cost fields if a pricing snapshot exists
- otherwise `pricing_snapshot=not_frozen`
- `CostPerValidRewrite` if pricing becomes available
- `CostPerAcceptedSpeedup` if pricing becomes available

## 7. Per-Case Record Schema

Each formal per-case record should include at minimum:

- `case_id`
- `pool`
- `route`
- `baseline_id`
- `source_sql_path`
- `candidate_sql_source`
- `execution_status`
- `result_consistency_status`
- `negative_guard_status` if applicable
- `row_count`
- `runtime_ms`
- `failure_category`
- `error_message`
- `validation_schema`
- `plan_source_path`
- `plan_candidate_path`
- `plan_parse_status`
- `token_usage_input` for LLM routes
- `token_usage_output` for LLM routes
- `token_usage_total` for LLM routes
- `artifact_claim_boundary`

Recommended interpretation fields:

- `source_runtime_ms`
- `candidate_runtime_ms`
- `speedup_ratio`
- `win_tie_loss_status`
- `timeout_applied`
- `plan_pair_available`
- `operator_delta_available`
- `attribution_available`

## 8. Formal Run Sequencing

Recommended execution order:

1. regenerate or validate native control records
2. run `NATIVE_IDENTITY`
3. run `HUMAN_REFERENCE_POSITIVE`
4. run `HARD_NEGATIVE_GUARD`
5. summarize controls
6. run `SQLGLOT_OPT_SAME_DIALECT`
7. run `LLM_DIRECT_REWRITE_STRONG` using existing per-case output mode or equivalent
8. execute extracted LLM SQL
9. run result consistency checks
10. collect and verify plans
11. produce the common-core rollup

Suggested output artifact paths:

- `reports/formal_common_core/native_identity_v0.json`
- `reports/formal_common_core/human_reference_positive_v0.json`
- `reports/formal_common_core/hard_negative_guard_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_v0.json`
- `reports/formal_common_core/common_core_rollup_v0.json`

These reports may remain git-ignored unless explicitly promoted later.

## 9. Gating Rules

- only result-consistent rewrites enter speedup statistics
- hard negatives must be rejected, not rewarded
- execution success alone is not correctness
- row-count match alone is not correctness
- LLM extraction success alone is not correctness
- plan metrics only apply when both source and candidate plan artifacts exist
- token cost is reported separately from correctness and speedup

## 10. Open Blockers

- formal result checker wiring may need confirmation
- plan collection and plan normalization may need confirmation
- pricing snapshot is not frozen
- repeated runtime policy is not frozen
- timeout policy is not frozen
- the formal denominator is still a proposal, not a registry admission decision

## 11. Recommended Next Action

- Implement a formal common-core preflight command that reads the 9-case denominator and verifies required source, rewrite, checker, result, and plan artifacts before running formal scoring.

## 12. Non-Goals / Claim Boundaries

- no registry writeback
- no admission decision
- no leaderboard result
- no correctness result yet
- no speedup result yet
- no formal review update

## 13. Verification / Non-Modification Note

- only this planning document was created
- no database workloads were run
- no SQL was executed
- no LLM calls were made
- no SQLGlot generation was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
