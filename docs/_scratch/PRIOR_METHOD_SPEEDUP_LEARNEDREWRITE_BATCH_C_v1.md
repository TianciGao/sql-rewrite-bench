# PRIOR_METHOD_SPEEDUP_LEARNEDREWRITE_BATCH_C_v1

## 0. Purpose And Boundary

State:
- PG-only correctness-gated speedup slice
- LearnedRewrite / embedded LLM4Rewrite only
- 2 eligible non-noop candidates only
- no model/API
- no generation rerun
- no source-like/no-op candidates
- no MySQL/Spark
- no cross-engine transfer
- not leaderboard

## 1. Eligibility Source

This batch follows the eligibility gate recorded in:
- [docs/_scratch/PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1.md)

Eligible non-noop cases:
- `PERF_0033`
- `PERF_0054`

Excluded LearnedRewrite cases were source-like/no-op candidates and were not included.

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
| `PERF_0033` | `0.321039` | `0.476698` | `0.673464` | `loss` | `true` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/learnedrewrite_llm4rewrite/PERF_0033/result_v1.json` |
| `PERF_0054` | `0.276432` | `0.469668` | `0.588569` | `loss` | `true` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/learnedrewrite_llm4rewrite/PERF_0054/result_v1.json` |

## 4. Method-level Metrics

- denominator = `2`
- valid_measured_count = `2`
- gm_speedup = `0.6295872209675301`
- win_count = `0`
- tie_count = `0`
- loss_count = `2`
- regression_count@20 = `2`
- measurement_failure_count = `0`
- timeout_count = `0`
- speedup_status = `measured`

## 5. Interpretation

This is bounded PG-only speedup evidence for LearnedRewrite’s checker-consistent non-noop candidates. It is not cross-engine transfer evidence and not a full leaderboard result.

The correctness gate came from prior checker-backed evidence and excluded source-like/no-op candidates by design. The measured runtimes are again sub-ms or near-sub-ms, so this batch should retain a witness-scale caveat in any paper-facing wording.

## 6. Recommended Next Step

`run LearnedRewrite speedup sanity audit`

## 7. Non-Modification Note

Confirm:
- only the 2 LearnedRewrite eligible candidates were targeted
- no model/API
- no LearnedRewrite generation rerun
- no no-op candidates
- no MySQL/Spark
- no SQLSolver/VeriEQL
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
