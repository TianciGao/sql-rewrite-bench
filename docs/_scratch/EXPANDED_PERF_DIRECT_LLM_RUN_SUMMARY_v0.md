# EXPANDED_PERF_DIRECT_LLM_RUN_SUMMARY_v0

## Status

This note records the completed expanded PERF Direct LLM full run from:

- `reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`

It is a documentation writeback only. It is not a new experiment, not a registry writeback, and not a final leaderboard artifact.

## Scope

- command family: `formal-expanded-perf-direct-llm-run`
- baseline: `LLM_DIRECT_REWRITE_STRONG`
- denominator: expanded PERF `34` cases
- engine scope: PostgreSQL only
- checker mode: report-local exact TSV checker
- run timestamp (UTC): `2026-05-04T18:42:43+00:00`

## Full-run outcome

- model calls: `34 / 34`
- extraction: `34 / 34`
- source PG execution: `34 / 34`
- candidate PG execution: `34 / 34`
- checker consistent: `34 / 34`
- row-count matches: `34 / 34`
- `ResultConsistencyRate=1.0`

No call, extraction, execution, or checker failures were recorded in the report summary.

## Token usage

- total token usage: `29414`
- token per consistent rewrite: `865.1176470588235`

## Claim boundary

This run supports only the following bounded claim:

- PostgreSQL-only
- checker-backed
- not a speedup result
- not a final leaderboard

Report claim-boundary string:

- `expanded_perf_direct_llm_pg_checker_not_speedup_not_final_leaderboard`

## Interpretation

The expanded PERF Direct LLM route is now closed as a checker-backed PostgreSQL execution line on the full 34-case expanded PERF packet. This closes the earlier seed-only status for correctness-style evidence, but it does not add any speedup claim and does not promote the route into a final ranking interpretation.

## Boundaries

- no registry changes
- no `docs/EXECUTION_STATUS.md` update
- no formal review update
- no speedup metrics added
- no cross-engine claim
