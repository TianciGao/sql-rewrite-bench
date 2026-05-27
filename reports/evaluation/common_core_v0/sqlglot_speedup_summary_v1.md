**SQLGlot Speedup Summary**
This is a SQLGlot-only same-engine speedup summary for `common_core_v0_40`. It is not a multi-method leaderboard, and Direct LLM / prior methods have not yet been rerun on the `common_core_v0_40` timing denominator.

Coverage-aware denominator context:
- `planned_same_engine_rows`: `240`
- `timing_eligible_rows`: `137`
- `timing_success_rows`: `137`
- `generation_failed`: `27`
- `noop_generated`: `24`
- `skipped_unsupported`: `36`
- `executed_failed`: `16`

Overall `GM_Speedup` is `1.0179` over `137` timing-success rows. Overall `RegressionRate@20%` is `0.0511` using the rule `speedup_ratio < 0.8`.
Coverage over planned denominator: `0.5708`. Coverage over timing-eligible denominator: `1.0000`.

Overall summary:
- `GM_Speedup`: `1.0179`
- `median_speedup_ratio`: `1.0075`
- `mean_speedup_ratio`: `1.0274`
- `min/p25/p75/max`: `0.5799` / `0.9908` / `1.0377` / `1.7537`
- `count_speedup_gt_1`: `84`
- `count_speedup_lt_1`: `53`
- `count_regression_lt_0_8`: `7`
- `RegressionRate@20%`: `0.0511`

By route:

| key | planned_rows | timing_eligible_rows | timing_success_rows | coverage_planned | coverage_eligible | GM_Speedup | median | mean | min | p25 | p75 | max | gt_1 | lt_1 | reg_lt_0.8 | reg_rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `sqlglot_optimize_same_dialect` | `120` | `65` | `65` | `0.5417` | `1.0000` | `1.0168` | `1.0110` | `1.0265` | `0.5799` | `0.9943` | `1.0403` | `1.7537` | `42` | `23` | `4` | `0.0615` |
| `sqlglot_transpile_same_dialect_noop` | `120` | `72` | `72` | `0.6000` | `1.0000` | `1.0190` | `1.0043` | `1.0283` | `0.6065` | `0.9798` | `1.0284` | `1.4564` | `42` | `30` | `3` | `0.0417` |

By engine:

| key | planned_rows | timing_eligible_rows | timing_success_rows | coverage_planned | coverage_eligible | GM_Speedup | median | mean | min | p25 | p75 | max | gt_1 | lt_1 | reg_lt_0.8 | reg_rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `pg` | `80` | `49` | `49` | `0.6125` | `1.0000` | `1.0213` | `1.0004` | `1.0459` | `0.5799` | `0.9798` | `1.1395` | `1.7537` | `26` | `23` | `7` | `0.1429` |
| `mysql` | `80` | `50` | `50` | `0.6250` | `1.0000` | `1.0062` | `1.0086` | `1.0064` | `0.9649` | `0.9941` | `1.0174` | `1.0469` | `33` | `17` | `0` | `0.0000` |
| `spark` | `80` | `38` | `38` | `0.4750` | `1.0000` | `1.0290` | `1.0159` | `1.0312` | `0.9234` | `0.9824` | `1.0480` | `1.1921` | `25` | `13` | `0` | `0.0000` |

By pool:

| key | planned_rows | timing_eligible_rows | timing_success_rows | coverage_planned | coverage_eligible | GM_Speedup | median | mean | min | p25 | p75 | max | gt_1 | lt_1 | reg_lt_0.8 | reg_rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `performance` | `96` | `56` | `56` | `0.5833` | `1.0000` | `1.0341` | `1.0103` | `1.0479` | `0.5799` | `0.9969` | `1.0381` | `1.7537` | `38` | `18` | `3` | `0.0536` |
| `consistency` | `54` | `36` | `36` | `0.6667` | `1.0000` | `1.0030` | `1.0089` | `1.0129` | `0.6065` | `0.9721` | `1.0439` | `1.3399` | `22` | `14` | `3` | `0.0833` |
| `longtail` | `36` | `36` | `36` | `1.0000` | `1.0000` | `1.0216` | `1.0035` | `1.0245` | `0.9335` | `0.9890` | `1.0284` | `1.3329` | `22` | `14` | `0` | `0.0000` |
| `portability` | `54` | `9` | `9` | `0.1667` | `1.0000` | `0.9650` | `0.9943` | `0.9699` | `0.7217` | `0.9915` | `0.9968` | `1.0423` | `2` | `7` | `1` | `0.1111` |

Interpretation boundaries:
- This file is a speedup summary, not a final same-engine leaderboard.
- It uses only timing-success rows for `GM_Speedup` and regression calculations.
- Direct LLM and prior methods are not yet rerun on `common_core_v0_40`, so no cross-method ranking claim is valid yet.
- No multi-method `same_engine_leaderboard.csv` is created here.
