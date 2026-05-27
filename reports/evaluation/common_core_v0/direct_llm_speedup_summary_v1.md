**Direct LLM Speedup Summary**
This is a Direct LLM-only same-engine speedup summary for `common_core_v0_40`. It is not a multi-method leaderboard.

Coverage-aware denominator context:
- `planned_rows`: `120`
- `generation_success_rows`: `120`
- `ready_to_execute_rows`: `115`
- `match_exact_rows`: `94`
- `timing_eligible_rows`: `94`
- `timing_success_rows`: `94`
- `timing_failed_rows_after_retry`: `0`
- `preflight_blocked`: `5`
- `execution_failed`: `16`
- `mismatch`: `5`

Resolved timing provenance:
- `89` timing-success rows are retained from `direct_llm_same_engine_timing_01`
- `5` Spark timing rows are replaced from `direct_llm_same_engine_timing_retry_spark_perf5_01`
- the retry rows are `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024` on `spark`

Overall `GM_Speedup` is `1.0436` over `94` timing-success rows. Overall `RegressionRate@20%` is `0.0319` using the rule `speedup_ratio < 0.8`.

Coverage:
- over planned denominator: `0.7833`
- over timing-eligible denominator: `1.0000`
- over ready-to-execute denominator: `0.8174`

Overall summary:
- `GM_Speedup`: `1.0436`
- `median_speedup_ratio`: `1.0094`
- `mean_speedup_ratio`: `1.0538`
- `min/p25/p75/max`: `0.6949` / `0.9889` / `1.0450` / `1.7075`
- `count_speedup_gt_1`: `57`
- `count_speedup_lt_1`: `37`
- `count_regression_lt_0.8`: `3`
- `RegressionRate@20%`: `0.0319`

By engine:

| key | planned_rows | ready_to_execute_rows | timing_eligible_rows | timing_success_rows | coverage_planned | coverage_eligible | coverage_ready | GM_Speedup | median | mean | min | p25 | p75 | max | gt_1 | lt_1 | reg_lt_0.8 | reg_rate | retry_rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mysql` | `40` | `38` | `34` | `34` | `0.8500` | `1.0000` | `0.8947` | `1.0016` | `1.0012` | `1.0018` | `0.9668` | `0.9898` | `1.0129` | `1.0380` | `18` | `16` | `0` | `0.0000` | `0` |
| `pg` | `40` | `39` | `32` | `32` | `0.8000` | `1.0000` | `0.8205` | `1.0948` | `1.0094` | `1.1203` | `0.6949` | `0.9888` | `1.3367` | `1.7075` | `19` | `13` | `3` | `0.0938` | `0` |
| `spark` | `40` | `38` | `28` | `28` | `0.7000` | `1.0000` | `0.7368` | `1.0386` | `1.0272` | `1.0408` | `0.9049` | `0.9946` | `1.0748` | `1.2619` | `20` | `8` | `0` | `0.0000` | `5` |

By pool:

| key | planned_rows | ready_to_execute_rows | timing_eligible_rows | timing_success_rows | coverage_planned | coverage_eligible | coverage_ready | GM_Speedup | median | mean | min | p25 | p75 | max | gt_1 | lt_1 | reg_lt_0.8 | reg_rate | retry_rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `consistency` | `27` | `27` | `24` | `24` | `0.8889` | `1.0000` | `0.8889` | `1.0445` | `1.0156` | `1.0571` | `0.7250` | `0.9890` | `1.0404` | `1.7075` | `14` | `10` | `1` | `0.0417` | `0` |
| `longtail` | `18` | `18` | `16` | `16` | `0.8889` | `1.0000` | `0.8889` | `1.0578` | `1.0163` | `1.0643` | `0.9049` | `0.9988` | `1.0528` | `1.3434` | `12` | `4` | `0` | `0.0000` | `0` |
| `performance` | `48` | `48` | `45` | `45` | `0.9375` | `1.0000` | `0.9375` | `1.0413` | `1.0027` | `1.0528` | `0.6949` | `0.9855` | `1.0703` | `1.6956` | `24` | `21` | `2` | `0.0444` | `5` |
| `portability` | `27` | `22` | `9` | `9` | `0.3333` | `1.0000` | `0.4091` | `1.0281` | `1.0052` | `1.0310` | `0.9841` | `1.0015` | `1.0092` | `1.2655` | `7` | `2` | `0` | `0.0000` | `0` |

Interpretation boundaries:
- This file is a Direct LLM-only speedup summary, not a multi-method leaderboard.
- `GM_Speedup` and `RegressionRate@20%` use only `94` timing-success rows from the resolved timing package.
- The five Spark retry rows remain part of the valid timing evidence and are already incorporated in the resolved summary.
- PORT rows still carry portability-stress caveats and should not be normalized into cross-method leaderboard claims by default.
- A SQLGlot comparison, if needed, belongs in a separate multi-method summary rather than this file.
