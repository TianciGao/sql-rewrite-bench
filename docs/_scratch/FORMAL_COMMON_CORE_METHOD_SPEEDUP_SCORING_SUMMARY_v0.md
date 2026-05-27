# FORMAL_COMMON_CORE_METHOD_SPEEDUP_SCORING_SUMMARY_v0

## Status

This is a correctness-gated PERF-only generated-method speedup summary from existing runtime reruns and existing checker-backed consistency artifacts.

No new runtime rerun was performed in this phase.

## Policy Basis

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`
- primary runtime statistic: `median`
- tie threshold: `0.05`
- regression threshold: `1.2`

## SQLGlot PERF-Only Speedup

- route: `SQLGLOT_OPT_SAME_DIALECT`
- consistency gate pass count: `7 / 7`
- `GM_Speedup=0.9709643241218479`
- `Win/Tie/Loss=1/2/4`
- `RegressionRate@20%=0/7`

## Direct LLM PERF-Only Speedup

- route: `LLM_DIRECT_REWRITE_STRONG`
- consistency gate pass count: `7 / 7`
- `GM_Speedup=1.0023345046000625`
- `Win/Tie/Loss=1/5/1`
- `RegressionRate@20%=0/7`

## LLM Token Note

- `total_token_usage=4487`
- `token_per_executed_case=641.0`
- token cost is reported beside runtime and is not folded into runtime

## Boundaries

- PERF-only
- correctness-gated for PERF-only generated methods
- CONS excluded from `GM_Speedup`
- not the full benchmark leaderboard
- no new runtime rerun in this phase
- no registry writeback
- no formal review update

