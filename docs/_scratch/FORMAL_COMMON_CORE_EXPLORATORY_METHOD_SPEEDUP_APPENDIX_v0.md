# FORMAL_COMMON_CORE_EXPLORATORY_METHOD_SPEEDUP_APPENDIX_v0

## Status

This is the exploratory row-count-gated method speedup appendix for the formal common-core PERF-only denominator.

It is appendix material only.

It is not correctness-gated leaderboard speedup.

## Policy Basis

- `docs/_scratch/FORMAL_COMMON_CORE_SPEEDUP_POLICY_DECISION_PACKET_v0.md`
- `reports/formal_common_core/human_positive_speedup_run_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/method_consistency_scoring_v0.json`
- `reports/formal_common_core/exploratory_method_speedup_appendix_v0.json`

Frozen execution policy used for this appendix:

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`
- `primary_runtime_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

## PERF-Only Denominator

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

## SQLGlot Same-Dialect Exploratory Result

- route: `SQLGLOT_OPT_SAME_DIALECT`
- `case_count=7`
- `success_count=7`
- `row_count_match_count=7`
- `exploratory_gm_speedup=0.9709643241218479`
- `Win/Tie/Loss=1/2/4`
- `RegressionRate@20%=0/7`

Per-case compact view:

| case_id | source median ms | candidate median ms | ratio | status |
|---|---:|---:|---:|---|
| `PERF_0006` | `0.296` | `0.277` | `1.0686` | `win` |
| `PERF_0008` | `0.294` | `0.290` | `1.0138` | `tie` |
| `PERF_0013` | `0.665` | `0.670` | `0.9925` | `tie` |
| `PERF_0017` | `0.387` | `0.410` | `0.9439` | `loss` |
| `PERF_0024` | `0.336` | `0.371` | `0.9057` | `loss` |
| `PERF_0033` | `0.301` | `0.318` | `0.9465` | `loss` |
| `PERF_0054` | `0.274` | `0.293` | `0.9352` | `loss` |

## Direct LLM Rewrite Exploratory Result

- route: `LLM_DIRECT_REWRITE_STRONG`
- `case_count=7`
- `success_count=7`
- `row_count_match_count=7`
- `exploratory_gm_speedup=1.0023345046000625`
- `Win/Tie/Loss=1/5/1`
- `RegressionRate@20%=0/7`
- `total_token_usage=4487`
- `token_per_executed_case=641.0`

Per-case compact view:

| case_id | source median ms | candidate median ms | ratio | status | token_usage_total |
|---|---:|---:|---:|---|---:|
| `PERF_0006` | `0.273` | `0.262` | `1.0420` | `tie` | `655` |
| `PERF_0008` | `0.363` | `0.332` | `1.0934` | `win` | `633` |
| `PERF_0013` | `0.658` | `0.702` | `0.9373` | `loss` | `709` |
| `PERF_0017` | `0.433` | `0.420` | `1.0310` | `tie` | `771` |
| `PERF_0024` | `0.399` | `0.406` | `0.9828` | `tie` | `699` |
| `PERF_0033` | `0.294` | `0.304` | `0.9671` | `tie` | `510` |
| `PERF_0054` | `0.272` | `0.280` | `0.9714` | `tie` | `510` |

## Boundary

- exploratory row-count-gated appendix only
- not correctness-gated
- not leaderboard
- row-count match is not semantic equivalence
- no route-specific checker-backed consistency exists yet for SQLGlot or Direct LLM
- PERF-only
- CONS excluded
- LLM token cost is reported beside runtime, not folded into runtime

## Recommended Next Action

- decide whether to build route-specific checker-backed consistency artifacts or keep SQLGlot and Direct LLM speedup in appendix only
