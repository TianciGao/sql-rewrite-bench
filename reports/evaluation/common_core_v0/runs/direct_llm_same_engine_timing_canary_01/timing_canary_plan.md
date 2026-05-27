# Direct LLM Same-Engine Timing Canary Plan

## Scope

This package prepares a human-run timing canary for Direct LLM same-engine measurement on a small Common-core v0 slice.

- `denominator_id`: `common_core_v0_40`
- `method_id`: `direct_llm`
- `route_id`: `direct_llm_same_engine_rewrite`
- canary cases: `PERF_0006`, `CONS_0010`, `LONGTAIL_0011`
- engines: `pg`, `mysql`, `spark`
- planned canary rows: `9`
- warmup_count: `1`
- repeat_count: `3`

## Eligibility

The canary includes only rows with `timing_eligible=yes` from:

- `reports/evaluation/common_core_v0/direct_llm_timing_preflight/direct_llm_timing_candidate_matrix.csv`

Observed scope result:

- selected rows: `9`
- timing_eligible rows: `9`
- speedup_eligible rows: `9`
- excluded rows in chosen case scope: `0`

## Row Breakdown

By engine:

- `pg`: `3`
- `mysql`: `3`
- `spark`: `3`

By pool:

- `performance`: `3`
- `consistency`: `3`
- `longtail`: `3`

## Runner Strategy

The human-run script:

- must be run from repo root
- sources `scripts/env_postgres.sh`, `scripts/env_mysql.sh`, and `scripts/env_spark.sh`
- reuses the corrected same-engine timing runner logic from the SQLGlot timing canary
- uses no `tmp_repo`
- records per-row timing JSON under `timings/<case_id>/<engine>/direct_llm_same_engine_rewrite.json`
- captures stdout/stderr logs
- writes `run_results.json`
- continues after row-level failures

## Boundaries

This canary package:

- does not execute anything by itself
- does not compute final `GM_Speedup`
- does not compute final `RegressionRate@20%`
- does not create any leaderboard
- is not a final performance summary

## Main Caveats

- The selected scope is clean: all `9` chosen rows are already `match_exact` and timing-eligible.
- This canary is still only a timing scaffolding package until a human executes the script.
- Timing success here should only be treated as an operational check before the later 94-row Direct LLM timing run.
