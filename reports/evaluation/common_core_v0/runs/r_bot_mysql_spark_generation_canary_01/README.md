# R-Bot MySQL/Spark Generation Canary 01

This package is a bounded human-run **generation canary** for six MySQL/Spark rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

It exists to answer a narrow question:

> are the old MySQL/Spark `unsupported` rows blocked by genuine method limits, or by the recovered harness and adapter path?

## Important boundary

This package is **not**:

- a full MySQL/Spark evaluation
- execution evidence
- timing evidence
- speedup evidence
- leaderboard evidence

## Current expected behavior

At the time this package was created, the visible upstream runtime still used a PostgreSQL-only `DBArgs` path. Because of that, the shell runner is intentionally fail-closed:

- if the adapter is still PostgreSQL-only, preflight writes explicit blocked status and exits before row attempts
- rows remain explicit in `run_event_long.csv`
- no rows are silently dropped

## Environment

- formal runtime:
  - `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python`
- formal Chroma index:
  - `/tmp/rewritebench_rbot_formal_chroma_index_01`
- retained formal index identifier:
  - `reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json`

Required environment visibility:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

The runner never writes the API key value.

## Optional provider preflight

The package reserves an optional provider preflight gate behind:

- `RBOT_CANARY_ALLOW_PROVIDER_PREFLIGHT_CALL=1`

That gate is off by default. When explicitly enabled later by a human-run action, the runner performs a secret-safe OpenAI-compatible auth probe and only records pass/fail status.
