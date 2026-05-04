# FORMAL_COMMON_CORE_SPEEDUP_PREFLIGHT_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the formal common-core speedup preflight state.

This is a preflight only.

No `GM_Speedup` has been computed.

## 2. Input Docs / Reports

- `docs/_scratch/FORMAL_COMMON_CORE_RUNTIME_SPEEDUP_POLICY_FREEZE_PLAN_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_RUNTIME_OBSERVATION_SNAPSHOT_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_CURRENT_RESULTS_SNAPSHOT_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_METHOD_CONSISTENCY_SCORING_SUMMARY_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_PLAN_PARSE_SUMMARY_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_PLAN_OPERATOR_DELTA_SUMMARY_v0.md`
- `reports/formal_common_core/runtime_observation_snapshot_v0.json`
- `reports/formal_common_core/control_scoring_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_scoring_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_scoring_v0.json`
- `reports/formal_common_core/method_consistency_scoring_v0.json`
- `reports/formal_common_core/plan_parse_summary_v0.json`
- `reports/formal_common_core/plan_operator_delta_summary_v0.json`
- `reports/formal_common_core/native_identity_execution_v0.json`
- `reports/formal_common_core/human_reference_positive_execution_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/speedup_preflight_v0.json`

## 3. Proposed Runtime Policy Read From Freeze Plan

Current proposed policy values recorded by the preflight:

- `repeat_count_proposed=5`
- `warmup_count_proposed=1`
- `statement_timeout_ms_proposed=30000`
- `primary_statistic_proposed=median`
- `tie_threshold_proposed=0.05`
- `regression_threshold_proposed=1.2`

Current freeze status:

- `runtime_policy_frozen=false`
- `speedup_metric_policy_frozen=false`

## 4. Runtime Availability

Runtime observation availability is complete at the single-run level:

- source runtime available: `9 / 9`
- human positive observed ratios available: `9 / 9`
- SQLGlot observed ratios available: `9 / 9`
- Direct LLM observed ratios available: `9 / 9`

Important boundary:

- current runtime ratios are single-run observations only
- no repeated measurement policy is frozen yet
- no warmup policy is frozen yet
- no formal speedup scoring has been run

## 5. Route Eligibility Table

| route | eligible count | blocked count | current interpretation |
|---|---:|---:|---|
| `NATIVE_IDENTITY` | `0` | `9` | source/control baseline only; not a scored speedup method |
| `HUMAN_REFERENCE_POSITIVE` | `7` | `2` | performance-pool cases are preflight-eligible; `CONS` cases remain policy-open |
| `SQLGLOT_OPT_SAME_DIALECT` | `0` | `9` | blocked for formal speedup by missing checker-backed method consistency |
| `LLM_DIRECT_REWRITE_STRONG` | `0` | `9` | blocked for formal speedup by missing checker-backed method consistency |

## 6. Main Blockers

Current blockers recorded in the report:

- `runtime_policy_not_frozen`
- `speedup_metric_policy_not_frozen`
- `checker_backed_method_consistency_missing_for_generated_methods`
- `consistency_pool_speedup_inclusion_policy_open`
- `runtime_observations_are_single_run_only`

Blocker counts:

- `method_consistency_blocker_count=14`
- `policy_blocker_count=6`

Generated-method interpretation:

- SQLGlot and Direct LLM both have execution success and row-count observations
- SQLGlot and Direct LLM are still blocked from formal speedup until checker-backed method consistency exists, or policy explicitly permits a row-count-only exploratory table

## 7. CONS Inclusion Policy Note

- `CONS_0007` and `CONS_0012` remain `policy_open / semantic_analysis_preferred`
- CONS cases should not automatically enter `GM_Speedup`
- current preflight keeps CONS cases outside formal speedup eligibility

## 8. Current Decision

- `formal_speedup_run_ready=false`
- `formal_speedup_scoring_complete=false`

The current repository state is sufficient to inspect runtime observations, plan-pair readiness, and operator-delta availability.

It is not sufficient to begin formal common-core speedup scoring.

## 9. Claim Boundaries

- current runtime ratios are single-run observations only
- no `GM_Speedup` has been computed
- no `RegressionRate` has been computed
- no speedup leaderboard claim exists
- no registry writeback occurred
- no formal review update occurred

## 10. Recommended Next Action

- freeze the formal runtime/speedup policy decision, including CONS inclusion and whether exploratory row-count-gated method speedup tables are allowed before checker-backed consistency exists
