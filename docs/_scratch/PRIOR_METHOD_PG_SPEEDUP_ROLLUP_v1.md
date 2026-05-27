# PRIOR_METHOD_PG_SPEEDUP_ROLLUP_v1

## 0. Purpose And Boundary

State:
- combined PG-only prior-method speedup rollup
- correctness-gated
- witness-scale
- not final leaderboard
- not cross-engine transfer
- no new experiment

## 1. Eligibility Gate Recap

Only checker-consistent non-noop candidates were included in this speedup slice.

- `R-Bot / LLM4Rewrite` eligible = `7`
- `LLM-R2` eligible = `9`
- `LearnedRewrite / embedded LLM4Rewrite` eligible = `2`
- `SQLSolver / VeriEQL` excluded as support-only baselines
- LearnedRewrite source-like/no-op candidates excluded from primary speedup

## 2. Method-level Speedup Table

| method | original_10case_denominator | eligible_speedup_denominator | valid_measured_count | gm_speedup | win_count | tie_count | loss_count | regression_count@20 | measurement_failure_count | timeout_count | speedup_status | claim_boundary |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `R-Bot / LLM4Rewrite` | `10` | `7` | `7` | `0.8804340264675553` | `0` | `2` | `5` | `2` | `0` | `0` | `measured` | `bounded_pg_only_rbot_speedup_slice_not_leaderboard` |
| `LLM-R2` | `10` | `9` | `9` | `0.9592371433387649` | `1` | `6` | `2` | `1` | `0` | `0` | `measured` | `bounded_pg_only_llmr2_speedup_slice_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | `10` | `2` | `2` | `0.6295872209675301` | `0` | `0` | `2` | `2` | `0` | `0` | `measured` | `bounded_pg_only_learnedrewrite_speedup_slice_not_leaderboard` |

## 3. Per-case Result Matrix

| method | case_id | source_median_ms | candidate_median_ms | speedup | win_tie_loss | regression_at_20 | artifact_path |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `PERF_0008` | `0.333101` | `0.370147` | `0.899915` | `loss` | `false` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0008/result_v1.json` |
| `R-Bot / LLM4Rewrite` | `PERF_0013` | `0.646842` | `0.642742` | `1.006379` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0013/result_v1.json` |
| `R-Bot / LLM4Rewrite` | `PERF_0017` | `0.365525` | `0.405834` | `0.900676` | `loss` | `false` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0017/result_v1.json` |
| `R-Bot / LLM4Rewrite` | `PERF_0024` | `0.361310` | `0.484327` | `0.746004` | `loss` | `true` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0024/result_v1.json` |
| `R-Bot / LLM4Rewrite` | `PERF_0052` | `0.347199` | `0.477033` | `0.727830` | `loss` | `true` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0052/result_v1.json` |
| `R-Bot / LLM4Rewrite` | `PERF_0054` | `0.285285` | `0.308523` | `0.924680` | `loss` | `false` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0054/result_v1.json` |
| `R-Bot / LLM4Rewrite` | `PERF_0063` | `0.392027` | `0.391501` | `1.001344` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/rbot_llm4rewrite/PERF_0063/result_v1.json` |
| `LLM-R2` | `PERF_0006` | `0.269075` | `0.283436` | `0.9493324771729773` | `loss` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0006/result_v1.json` |
| `LLM-R2` | `PERF_0008` | `0.345385` | `0.303515` | `1.137950348417706` | `win` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0008/result_v1.json` |
| `LLM-R2` | `PERF_0013` | `0.640059` | `0.639332` | `1.001137124373565` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0013/result_v1.json` |
| `LLM-R2` | `PERF_0017` | `0.364906` | `0.364709` | `1.0005401566728542` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0017/result_v1.json` |
| `LLM-R2` | `PERF_0019` | `0.302769` | `0.302581` | `1.0006213212329922` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0019/result_v1.json` |
| `LLM-R2` | `PERF_0024` | `0.372070` | `0.578988` | `0.6426212633077025` | `loss` | `true` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0024/result_v1.json` |
| `LLM-R2` | `PERF_0033` | `0.275261` | `0.277321` | `0.9925717850433252` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0033/result_v1.json` |
| `LLM-R2` | `PERF_0052` | `0.326110` | `0.333397` | `0.9781431746536412` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0052/result_v1.json` |
| `LLM-R2` | `PERF_0054` | `0.282526` | `0.277577` | `1.0178292870086498` | `tie` | `false` | `/tmp/rewritebench_prior_method_speedup/llmr2/PERF_0054/result_v1.json` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0033` | `0.321039` | `0.476698` | `0.6734641219388376` | `loss` | `true` | `/tmp/rewritebench_prior_method_speedup/learnedrewrite_llm4rewrite/PERF_0033/result_v1.json` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0054` | `0.276432` | `0.469668` | `0.5885689465750276` | `loss` | `true` | `/tmp/rewritebench_prior_method_speedup/learnedrewrite_llm4rewrite/PERF_0054/result_v1.json` |

## 4. Cross-method Interpretation

- `R-Bot / LLM4Rewrite`: correctness-gated nontrivial candidates did not yield speedup in this witness-scale slice; `0` wins, `2` ties, `5` losses.
- `LLM-R2`: mostly tie behavior, with `1` win, `6` ties, and `2` losses; `gm_speedup` remained below `1`.
- `LearnedRewrite / embedded LLM4Rewrite`: only two non-noop candidates entered primary speedup, and both regressed.
- Overall: checker consistency does not imply performance improvement.

## 5. Witness-scale Caveat

All three batches were sub-ms or near-sub-ms. This makes the slice useful as bounded harness and behavioral evidence, but not as a production-scale performance result and not as a final leaderboard.

Safe wording:

“Across the correctness-gated PG-only witness-scale speedup slice, the three integrated prior methods rarely improved runtime despite passing semantic checks. R-Bot had 0 wins over 7 eligible candidates, LLM-R2 had 1 win over 9, and LearnedRewrite’s two non-noop candidates both regressed. This result is not a final performance leaderboard; it shows that semantic validity and nontrivial candidate generation do not guarantee even witness-scale speedup.”

## 6. Metrics Used

Use:
- `gm_speedup`
- `win/tie/loss`
- `regression_count@20`
- `valid_measured_count`
- `measurement_failure_count`
- `timeout_count`

Do not use:
- `SpeedupTransferRate`
- cross-engine executable rate
- SQLSolver / VeriEQL support metrics
- leaderboard rank

## 7. Recommended Next Step

`update prior-method evidence summary with speedup slice`

## 8. Non-Modification Note

Confirm:
- no experiments run
- no model/API
- no DB
- no speedup rerun
- no checker
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
