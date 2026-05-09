# R-Bot MySQL/Spark Generation Canary Plan

## Purpose

This package is a bounded **generation-only feasibility canary** for testing whether the recovered formal R-Bot harness can be extended beyond PostgreSQL.

It is **not** a full MySQL/Spark evaluation and does **not** update the retained PostgreSQL result cards.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `source_denominator_id = common_core_v0_40_same_engine_120`
- `canary_denominator_id = r_bot_mysql_spark_generation_canary_01`
- engines: `mysql`, `spark`
- cases:
  - `PERF_0006`
  - `PERF_0007`
  - `CONS_0005`
- planned rows: `6`

## Why these six rows

- each selected case already has retained PostgreSQL generation evidence
- each selected case has both MySQL and Spark schema files
- each selected case has both MySQL and Spark witness-data files
- the scope is intentionally small enough to separate harness feasibility from benchmark-claim expansion

## Current blocker model

The visible upstream runtime still exposes a PostgreSQL-only adapter in `my_rewriter/database.py`. Because of that, this canary runner is intentionally fail-closed:

- if the non-PostgreSQL route is still unsafe, the package preflight stops before row attempts
- the script writes explicit package-level and row-level blocked status rather than silently dropping rows

## Planned preflight

The shell runner checks:

1. formal runtime path exists
2. formal Chroma index directory exists
3. formal Chroma index identifier exists
4. required environment visibility:
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL`
5. canary source/schema/witness paths exist
6. visible upstream LLM4Rewrite tree exists
7. upstream database adapter is not still PostgreSQL-only

If the adapter check fails, the runner writes:

- `run_results.json`
- `run_event_long.csv`

and stops before any row attempt.

## Optional provider preflight

The runner includes an optional provider auth probe only when:

- `RBOT_CANARY_ALLOW_PROVIDER_PREFLIGHT_CALL=1`

That preflight is off by default. When enabled later by a human-run action, it probes an OpenAI-compatible `/models` endpoint using the visible key and base URL without writing the key value.

## Claim boundary

This package can only produce:

- MySQL/Spark **generation canary** evidence

It cannot support:

- execution validity claims
- timing or speedup claims
- leaderboard claims
- method-comparison updates

## Expected next decision boundary

- if preflight fails on the adapter route, the next patch target is engine-adapter recovery
- if preflight passes and some rows generate, the next package should be engine-specific execution/validity for only the generated rows
