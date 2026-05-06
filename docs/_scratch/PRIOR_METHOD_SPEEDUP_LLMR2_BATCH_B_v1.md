# PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_v1

## 0. Purpose And Boundary

State:
- PG-only correctness-gated speedup slice
- LLM-R2 only
- 9 eligible candidates only
- no model/API
- no generation rerun
- no MySQL/Spark
- no cross-engine transfer
- not leaderboard

## 1. Eligibility Source

This batch follows the eligibility gate recorded in:
- [docs/_scratch/PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1.md)

Eligible cases:
- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`

Explicit exclusion:
- `PERF_0063` was excluded because LLM-R2 failed before generation at logical-plan probe time.

## 2. Runtime Policy

- engine: `PostgreSQL`
- measured repeats: `5` source + `5` candidate
- warmup policy: `1` optional warmup per query, excluded from metrics
- timeout policy: `60s` wall timeout per execution
- isolation/cleanup: isolated per-case schema with teardown after measurement
- speedup formula: `source_median_ms / candidate_median_ms`
- win threshold: `speedup >= 1.05`
- loss threshold: `speedup <= 0.95`
- tie band: otherwise
- `regression@20 = true` when `candidate_median_ms >= 1.20 * source_median_ms`

## 3. Per-case Result Table

| case_id | source_median_ms | candidate_median_ms | speedup | win_tie_loss | regression_at_20 | source_execution_status | candidate_execution_status | failure_category | artifact_paths |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `0.269075` | `0.283436` | `0.949332` | `loss` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0006/result_v1.json` |
| `PERF_0008` | `0.345385` | `0.303515` | `1.137950` | `win` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0008/result_v1.json` |
| `PERF_0013` | `0.640059` | `0.639332` | `1.001137` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0013/result_v1.json` |
| `PERF_0017` | `0.364906` | `0.364709` | `1.000540` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0017/result_v1.json` |
| `PERF_0019` | `0.302769` | `0.302581` | `1.000621` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0019/result_v1.json` |
| `PERF_0024` | `0.372070` | `0.578988` | `0.642621` | `loss` | `true` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0024/result_v1.json` |
| `PERF_0033` | `0.275261` | `0.277321` | `0.992572` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0033/result_v1.json` |
| `PERF_0052` | `0.326110` | `0.333397` | `0.978143` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0052/result_v1.json` |
| `PERF_0054` | `0.282526` | `0.277577` | `1.017829` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0054/result_v1.json` |

## 4. Method-level Metrics

- denominator = `9`
- valid_measured_count = `9`
- gm_speedup = `0.9592371433387649`
- win_count = `1`
- tie_count = `6`
- loss_count = `2`
- regression_count@20 = `1`
- measurement_failure_count = `0`
- timeout_count = `0`
- speedup_status = `measured`

## 5. Interpretation

This is bounded PG-only speedup evidence for LLM-R2’s checker-consistent clean candidates. It is not cross-engine transfer evidence and not a full leaderboard result.

The correctness gate came from prior checker-backed evidence, including the extraction cleanup for `PERF_0019`, `PERF_0024`, and `PERF_0052` where relevant. The measured runtimes are again sub-ms or near-sub-ms, so the batch should retain a witness-scale caveat in any paper-facing wording.

## 6. Recommended Next Step

`run LLM-R2 speedup sanity audit`

## 7. Non-Modification Note

Confirm:
- only the 9 LLM-R2 eligible candidates were targeted
- no model/API
- no LLM-R2 generation rerun
- no MySQL/Spark
- no SQLSolver/VeriEQL
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
