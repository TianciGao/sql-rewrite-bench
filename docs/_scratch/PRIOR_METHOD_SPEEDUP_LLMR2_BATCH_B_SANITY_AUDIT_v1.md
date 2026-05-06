# PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_SANITY_AUDIT_v1

## 0. Purpose And Boundary

This note is a read-only sanity audit of the bounded LLM-R2 PG-only speedup batch.

- no SQL execution
- no speedup rerun
- no model/API
- no DB
- no checker
- no registry writeback

## 1. Source Artifacts

Artifacts inspected:

- summary report: `docs/_scratch/PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_v1.md`
- method JSON: `/tmp/rewritebench_prior_method_speedup_llmr2_batch_b_v1.json`
- per-case result root: `/tmp/rewritebench_prior_method_speedup/llmr2/`

Expected case list:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`

Artifact presence result:

- all 9 expected cases are present in the method-level JSON
- all 9 per-case `result_v1.json` files are present
- no expected case artifact is missing

## 2. Runtime Array / Repeat Check

Each inspected per-case artifact includes measured runtime arrays for both source and candidate.

| case_id | source run count | candidate run count | warmup policy visible | measured arrays present |
|---|---:|---:|---|---|
| `PERF_0006` | 5 | 5 | yes | yes |
| `PERF_0008` | 5 | 5 | yes | yes |
| `PERF_0013` | 5 | 5 | yes | yes |
| `PERF_0017` | 5 | 5 | yes | yes |
| `PERF_0019` | 5 | 5 | yes | yes |
| `PERF_0024` | 5 | 5 | yes | yes |
| `PERF_0033` | 5 | 5 | yes | yes |
| `PERF_0052` | 5 | 5 | yes | yes |
| `PERF_0054` | 5 | 5 | yes | yes |

Warmup runs are excluded from the stored runtime arrays. The batch report’s runtime policy states 5 measured repeats, with 1 optional warmup outside the metric arrays.

## 3. Metric Recalculation

Per-case recomputation matched the stored artifacts.

| case_id | source median ms | candidate median ms | recomputed speedup | reported speedup | W/T/L check | regression@20 check |
|---|---:|---:|---:|---:|---|---|
| `PERF_0006` | 0.269075 | 0.283436 | 0.949332 | 0.949332 | match: `loss` | match: `false` |
| `PERF_0008` | 0.345385 | 0.303515 | 1.137950 | 1.137950 | match: `win` | match: `false` |
| `PERF_0013` | 0.640059 | 0.639332 | 1.001137 | 1.001137 | match: `tie` | match: `false` |
| `PERF_0017` | 0.364906 | 0.364709 | 1.000540 | 1.000540 | match: `tie` | match: `false` |
| `PERF_0019` | 0.302769 | 0.302581 | 1.000621 | 1.000621 | match: `tie` | match: `false` |
| `PERF_0024` | 0.372070 | 0.578988 | 0.642621 | 0.642621 | match: `loss` | match: `true` |
| `PERF_0033` | 0.275261 | 0.277321 | 0.992572 | 0.992572 | match: `tie` | match: `false` |
| `PERF_0052` | 0.326110 | 0.333397 | 0.978143 | 0.978143 | match: `tie` | match: `false` |
| `PERF_0054` | 0.282526 | 0.277577 | 1.017829 | 1.017829 | match: `tie` | match: `false` |

Checks applied:

- speedup = `source_median_ms / candidate_median_ms`
- `win` if speedup `>= 1.05`
- `loss` if speedup `<= 0.95`
- `tie` otherwise
- `regression_at_20 = true` if `candidate_median_ms >= 1.20 * source_median_ms`

All per-case checks passed.

## 4. Method-level Recalculation

Method-level recomputation also matched the stored batch summary.

- recomputed `gm_speedup = 0.9592371433387649`
- reported `gm_speedup = 0.9592371433387649`
- recomputed `win_count = 1`
- recomputed `tie_count = 6`
- recomputed `loss_count = 2`
- recomputed `regression_count@20 = 1`
- recomputed `measurement_failure_count = 0`
- recomputed `timeout_count = 0`

No metric mismatch was found in the inspected artifacts.

## 5. Witness-scale Caveat

All measured runtimes are sub-ms or near-sub-ms. This means the slice is useful as a bounded harness sanity check, but it should be described conservatively in any paper-facing narrative.

Safe wording:

“LLM-R2’s checker-consistent clean candidates showed mostly tie behavior with one win and two losses in the bounded PG-only witness-scale speedup slice; this slice is not a final performance leaderboard.”

The artifact evidence supports a bounded PG-only witness-scale speedup slice, not a final performance claim, not a production-scale study, and not a cross-engine result.

## 6. Classification

`measurement_sanity_passed_with_witness_scale_caveat`

## 7. Recommended Next Step

`run LearnedRewrite PG-only speedup batch`

## 8. Non-Modification Note

Confirmed:

- no baseline rerun
- no model/API
- no DB
- no checker
- no speedup rerun
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
