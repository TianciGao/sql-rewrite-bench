# PRIOR_METHOD_SPEEDUP_RBOT_BATCH_A_v1

## 0. Purpose And Boundary
State:
- PG-only correctness-gated speedup slice
- `R-Bot / LLM4Rewrite` only
- 7 eligible candidates only
- no model/API
- no generation rerun
- no MySQL/Spark
- no cross-engine transfer
- not leaderboard

## 1. Eligibility Source
Source preflight file:
- [docs/_scratch/PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1.md)

Eligible cases included:
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

Excluded and not included:
- `PERF_0006` checker-inconsistent
- `PERF_0019` generation/path failure
- `PERF_0033` generation/path failure

## 2. Runtime Policy
Report:
- engine: PostgreSQL only
- repeats: `5`
- warmup policy: `1` source warmup + `1` candidate warmup, not included in metrics
- timeout policy: `60s` wall timeout per execution via PostgreSQL `statement_timeout`
- isolation/cleanup policy: per-case isolated schema with DDL + witness load, then schema drop
- speedup formula: `source_median_ms / candidate_median_ms`
- win/tie/loss thresholds:
  - win if `speedup >= 1.05`
  - loss if `speedup <= 0.95`
  - tie otherwise
- regression@20 definition:
  - true if `candidate_median_ms >= 1.20 * source_median_ms`

## 3. Per-case Result Table
| case_id | source_median_ms | candidate_median_ms | speedup | win_tie_loss | regression_at_20 | source_execution_status | candidate_execution_status | failure_category | artifact_paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0008` | `0.333101` | `0.370147` | `0.899915` | `loss` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0008/result_v1.json` |
| `PERF_0013` | `0.646842` | `0.642742` | `1.006379` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0013/result_v1.json` |
| `PERF_0017` | `0.365525` | `0.405834` | `0.900676` | `loss` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0017/result_v1.json` |
| `PERF_0024` | `0.361310` | `0.484327` | `0.746004` | `loss` | `true` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0024/result_v1.json` |
| `PERF_0052` | `0.347199` | `0.477033` | `0.727830` | `loss` | `true` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0052/result_v1.json` |
| `PERF_0054` | `0.285285` | `0.308523` | `0.924680` | `loss` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0054/result_v1.json` |
| `PERF_0063` | `0.392027` | `0.391501` | `1.001344` | `tie` | `false` | `success` | `success` | `none` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0063/result_v1.json` |

## 4. Method-level Metrics
Report:
- denominator = `7`
- valid_measured_count = `7`
- `gm_speedup = 0.880434`
- win_count = `0`
- tie_count = `2`
- loss_count = `5`
- regression_count@20 = `2`
- measurement_failure_count = `0`
- timeout_count = `0`
- speedup_status = `measured`

## 5. Interpretation
This is bounded PG-only speedup evidence for `R-Bot / LLM4Rewrite`, not cross-engine transfer and not a full leaderboard result. The correctness gate came from earlier checker-backed prior-method evidence, so this slice measures only already-cleared candidates rather than generation-time quality.

Within this bounded batch, no case reached the `win` threshold. Two cases were ties (`PERF_0013`, `PERF_0063`) and five were losses. Two losses (`PERF_0024`, `PERF_0052`) also met the `regression@20` condition.

## 6. Recommended Next Step
- `pause for human review`

## 7. Non-Modification Note
Confirm:
- only the 7 R-Bot eligible candidates were targeted
- no model/API
- no R-Bot generation rerun
- no MySQL/Spark
- no SQLSolver/VeriEQL
- no registry/review/rules/EXECUTION_STATUS/case changes
