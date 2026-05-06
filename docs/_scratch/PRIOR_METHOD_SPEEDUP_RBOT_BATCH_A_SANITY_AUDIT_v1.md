# PRIOR_METHOD_SPEEDUP_RBOT_BATCH_A_SANITY_AUDIT_v1

## 0. Purpose And Boundary

This note is a read-only sanity audit of the bounded R-Bot / LLM4Rewrite PG-only speedup batch.

- no SQL execution
- no speedup rerun
- no model/API
- no DB access
- no checker
- no registry writeback

## 1. Source Artifacts

Artifacts inspected:

- summary report: `docs/_scratch/PRIOR_METHOD_SPEEDUP_RBOT_BATCH_A_v1.md`
- method JSON: `/tmp/rewritebench_prior_method_speedup_rbot_batch_a_v1.json`
- per-case result root: `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/`

Expected case list:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

Artifact presence result:

- all 7 expected cases are present in the method-level JSON
- all 7 per-case `result_v1.json` files are present
- no expected case artifact is missing

## 2. Runtime Array / Repeat Check

Each inspected per-case artifact includes measured runtime arrays for both source and candidate.

| case_id | source run count | candidate run count | warmup policy visible | measured arrays present |
|---|---:|---:|---|---|
| `PERF_0008` | 5 | 5 | yes | yes |
| `PERF_0013` | 5 | 5 | yes | yes |
| `PERF_0017` | 5 | 5 | yes | yes |
| `PERF_0024` | 5 | 5 | yes | yes |
| `PERF_0052` | 5 | 5 | yes | yes |
| `PERF_0054` | 5 | 5 | yes | yes |
| `PERF_0063` | 5 | 5 | yes | yes |

Warmup runs are excluded from the stored runtime arrays. The batch report’s runtime policy states 5 measured repeats, with optional warmup outside the metric arrays.

## 3. Metric Recalculation

Per-case recomputation matched the stored artifacts.

| case_id | source median ms | candidate median ms | recomputed speedup | reported speedup | W/T/L check | regression@20 check |
|---|---:|---:|---:|---:|---|---|
| `PERF_0008` | 0.333101 | 0.370147 | 0.899915 | 0.899915 | match: `loss` | match: `false` |
| `PERF_0013` | 0.646842 | 0.642742 | 1.006379 | 1.006379 | match: `tie` | match: `false` |
| `PERF_0017` | 0.365525 | 0.405834 | 0.900676 | 0.900676 | match: `loss` | match: `false` |
| `PERF_0024` | 0.361310 | 0.484327 | 0.746004 | 0.746004 | match: `loss` | match: `true` |
| `PERF_0052` | 0.347199 | 0.477033 | 0.727830 | 0.727830 | match: `loss` | match: `true` |
| `PERF_0054` | 0.285285 | 0.308523 | 0.924680 | 0.924680 | match: `loss` | match: `false` |
| `PERF_0063` | 0.392027 | 0.391501 | 1.001344 | 1.001344 | match: `tie` | match: `false` |

Checks applied:

- speedup = `source_median_ms / candidate_median_ms`
- `win` if speedup `>= 1.05`
- `loss` if speedup `<= 0.95`
- `tie` otherwise
- `regression_at_20 = true` if `candidate_median_ms >= 1.20 * source_median_ms`

All per-case checks passed.

## 4. Method-level Recalculation

Method-level recomputation also matched the stored batch summary.

- recomputed `gm_speedup = 0.8804340264675553`
- reported `gm_speedup = 0.8804340264675553`
- recomputed `win_count = 0`
- recomputed `tie_count = 2`
- recomputed `loss_count = 5`
- recomputed `regression_count@20 = 2`
- recomputed `measurement_failure_count = 0`
- recomputed `timeout_count = 0`

No metric mismatch was found in the inspected artifacts.

## 5. Witness-scale Caveat

All measured runtimes are sub-ms or near-sub-ms. This means the slice is useful as a bounded harness sanity check, but it should be described conservatively in any paper-facing narrative.

Safe wording:

“R-Bot’s checker-consistent nontrivial candidates did not yield speedup in the bounded PG-only witness-scale speedup slice; this slice is not a final performance leaderboard.”

The artifact evidence supports a bounded PG-only witness-scale speedup slice, not a final performance claim, not a production-scale study, and not a cross-engine result.

## 6. Classification

`measurement_sanity_passed_with_witness_scale_caveat`

## 7. Recommended Next Step

`run LLM-R2 PG-only speedup batch`

## 8. Non-Modification Note

Confirmed:

- no baseline rerun
- no model/API
- no DB
- no checker
- no speedup rerun
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
