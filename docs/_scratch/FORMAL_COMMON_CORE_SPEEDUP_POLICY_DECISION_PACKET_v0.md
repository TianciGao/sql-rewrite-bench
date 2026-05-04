# FORMAL_COMMON_CORE_SPEEDUP_POLICY_DECISION_PACKET_v0

## 1. Status

This is a tracked scratch policy decision packet for the first formal common-core speedup pass.

It freezes policy for the next speedup run plan.

It is not a speedup result.

## 2. Inputs / Preflight Basis

- `docs/_scratch/FORMAL_COMMON_CORE_SPEEDUP_PREFLIGHT_SUMMARY_v0.md`
- `reports/formal_common_core/speedup_preflight_v0.json`
- `docs/_scratch/FORMAL_COMMON_CORE_RUNTIME_SPEEDUP_POLICY_FREEZE_PLAN_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_RUNTIME_OBSERVATION_SNAPSHOT_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_CURRENT_RESULTS_SNAPSHOT_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_METHOD_CONSISTENCY_SCORING_SUMMARY_v0.md`

Preflight basis carried into this decision:

- `formal_speedup_run_ready=false`
- `runtime_policy_frozen=false`
- `speedup_metric_policy_frozen=false`
- `HUMAN_REFERENCE_POSITIVE`: `7` eligible, `2` blocked
- `SQLGLOT_OPT_SAME_DIALECT`: `0` eligible, `9` blocked
- `LLM_DIRECT_REWRITE_STRONG`: `0` eligible, `9` blocked

## 3. Decision Summary

The first formal common-core speedup-pass policy is frozen as:

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`
- `primary_runtime_statistic=median`
- auxiliary runtime statistics: `min`, `mean`
- `tie_threshold=±5%`
- `regression_threshold=20%`

## 4. Denominator Decision

`GM_Speedup` first pass is `PERF`-only.

PERF denominator:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

`CONS_0007` and `CONS_0012` are excluded from the first `GM_Speedup` pass.

Consistency-pool cases remain correctness / semantic analysis only for this first pass.

## 5. Route Eligibility Decision

| route | status | reason |
|---|---|---|
| `NATIVE_IDENTITY` | baseline_only | source/control baseline; not scored as a speedup method |
| `HUMAN_REFERENCE_POSITIVE` | perf_only_eligible | eligible for PERF-only positive-control speedup |
| `HARD_NEGATIVE_GUARD` | excluded | excluded from the speedup leaderboard |
| `SQLGLOT_OPT_SAME_DIALECT` | blocked | blocked from correctness-gated speedup until route-specific checker-backed consistency exists |
| `LLM_DIRECT_REWRITE_STRONG` | blocked | blocked from correctness-gated speedup until route-specific checker-backed consistency exists |
| `SQLGlot / LLM exploratory appendix` | caveated_only | allowed only if explicitly labeled row-count-gated exploratory and not leaderboard |

## 6. LLM Cost Decision

- LLM token cost should be reported beside speedup
- LLM token cost is not folded into runtime
- `pricing_snapshot` remains `not_frozen` unless explicitly frozen later

## 7. What This Enables Next

- `HUMAN_REFERENCE_POSITIVE` PERF-only formal speedup preflight / run can proceed under this frozen policy
- SQLGlot and Direct LLM formal speedup remain blocked for leaderboard scoring
- exploratory SQLGlot / Direct LLM speedup tables may be considered only with explicit caveats

## 8. Claim Boundaries

- no speedup computed
- no `GM_Speedup` computed
- no `RegressionRate` computed
- no leaderboard claim
- no registry writeback
- no admission decision
- no formal review update

## 9. Recommended Next Action

- implement `HUMAN_REFERENCE_POSITIVE` PERF-only formal speedup run preflight using the frozen policy

## 10. Verification / Non-Modification Note

- only this packet was created
- no database workloads were run
- no SQL was executed
- no LLM calls were made
- no SQLGlot generation was run
- no checker was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
