# PRIOR_METHOD_SPEEDUP_LEARNEDREWRITE_BATCH_C_SANITY_AUDIT_v1

## 0. Purpose And Boundary

This note is a read-only sanity audit of the bounded LearnedRewrite / embedded LLM4Rewrite PG-only speedup batch.

- no SQL execution
- no speedup rerun
- no model/API
- no DB
- no checker
- no registry writeback

## 1. Source Artifacts

Artifacts inspected:

- summary report: `docs/_scratch/PRIOR_METHOD_SPEEDUP_LEARNEDREWRITE_BATCH_C_v1.md`
- method JSON: `/tmp/rewritebench_prior_method_speedup_learnedrewrite_batch_c_v1.json`
- per-case result root: `/tmp/rewritebench_prior_method_speedup/learnedrewrite_llm4rewrite/`

Expected case list:

- `PERF_0033`
- `PERF_0054`

Artifact presence result:

- both expected cases are present in the method-level JSON
- both per-case `result_v1.json` files are present
- no expected case artifact is missing

## 2. Runtime Array / Repeat Check

Each inspected per-case artifact includes measured runtime arrays for both source and candidate.

| case_id | source run count | candidate run count | warmup policy visible | measured arrays present |
|---|---:|---:|---|---|
| `PERF_0033` | 5 | 5 | yes | yes |
| `PERF_0054` | 5 | 5 | yes | yes |

Warmup runs are excluded from the stored runtime arrays. The batch report’s runtime policy states 5 measured repeats, with 1 optional warmup outside the metric arrays.

## 3. Metric Recalculation

Per-case recomputation matched the stored artifacts.

| case_id | source median ms | candidate median ms | recomputed speedup | reported speedup | W/T/L check | regression@20 check |
|---|---:|---:|---:|---:|---|---|
| `PERF_0033` | 0.321039 | 0.476698 | 0.673464 | 0.673464 | match: `loss` | match: `true` |
| `PERF_0054` | 0.276432 | 0.469668 | 0.588569 | 0.588569 | match: `loss` | match: `true` |

Checks applied:

- speedup = `source_median_ms / candidate_median_ms`
- `win` if speedup `>= 1.05`
- `loss` if speedup `<= 0.95`
- `tie` otherwise
- `regression_at_20 = true` if `candidate_median_ms >= 1.20 * source_median_ms`

All per-case checks passed.

## 4. Method-level Recalculation

Method-level recomputation also matched the stored batch summary.

- recomputed `gm_speedup = 0.6295872209675301`
- reported `gm_speedup = 0.6295872209675301`
- recomputed `win_count = 0`
- recomputed `tie_count = 0`
- recomputed `loss_count = 2`
- recomputed `regression_count@20 = 2`
- recomputed `measurement_failure_count = 0`
- recomputed `timeout_count = 0`

No metric mismatch was found in the inspected artifacts.

## 5. Witness-scale Caveat

All measured runtimes are sub-ms or near-sub-ms. This means the slice is useful as a bounded harness sanity check, but it should be described conservatively in any paper-facing narrative.

Safe wording:

“LearnedRewrite’s two checker-consistent non-noop candidates both regressed in the bounded PG-only witness-scale speedup slice; this slice is not a final performance leaderboard.”

The artifact evidence supports a bounded PG-only witness-scale speedup slice, not a final performance claim, not a production-scale study, and not a cross-engine result.

## 6. Classification

`measurement_sanity_passed_with_witness_scale_caveat`

## 7. Recommended Next Step

`create combined prior-method PG speedup rollup`

## 8. Non-Modification Note

Confirmed:

- no baseline rerun
- no model/API
- no DB
- no checker
- no speedup rerun
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
