# EXPANDED_PERF_DIRECT_LLM_SPEEDUP_PREFLIGHT_SUMMARY_v0

## Status

This note records the expanded PERF Direct LLM speedup preflight from:

- `reports/formal_expansion/expanded_perf_direct_llm_speedup_preflight_v0.json`

It is a preflight-only writeback. It is not a speedup result, not a model call, and not a runtime repeat run.

## Scope

- command: `formal-expanded-perf-direct-llm-speedup-preflight`
- prior input report: `reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`
- prior summary input: `docs/_scratch/EXPANDED_PERF_DIRECT_LLM_RUN_SUMMARY_v0.md`
- denominator: expanded PERF `34` cases
- route: `LLM_DIRECT_REWRITE_STRONG`
- engine scope: PostgreSQL only

## Checked readiness conditions

For each of the 34 expanded PERF cases, the preflight checked:

- source materialization exists
- candidate materialization exists
- `checker_status=consistent`
- source SQL path exists
- extracted candidate SQL is recoverable from the prior run report
- validation schema is available
- runtime policy is defined

Runtime policy carried by the preflight:

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- `primary_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

## Outcome

- ready count: `34`
- blocked count: `0`
- ready fraction: `34 / 34`
- blocked fraction: `0 / 34`
- blockers by type: none
- total token usage carried from prior run: `29414`

Ready cases:

- `PERF_0007`, `PERF_0009`, `PERF_0010`, `PERF_0011`, `PERF_0012`, `PERF_0014`, `PERF_0015`, `PERF_0016`, `PERF_0018`, `PERF_0019`, `PERF_0020`, `PERF_0021`, `PERF_0022`, `PERF_0023`, `PERF_0025`, `PERF_0026`, `PERF_0034`, `PERF_0035`, `PERF_0036`, `PERF_0043`, `PERF_0044`, `PERF_0047`, `PERF_0050`, `PERF_0052`, `PERF_0053`, `PERF_0056`, `PERF_0062`, `PERF_0063`, `PERF_0065`, `PERF_0066`, `PERF_0027`, `PERF_0028`, `PERF_0030`, `PERF_0031`

Blocked cases:

- none

## Execute-refused guardrail

The command correctly refuses `--execute` and writes:

- `reports/formal_expansion/expanded_perf_direct_llm_speedup_preflight_execute_refused_v0.json`

This keeps the command inside the requested boundary: preflight only, with no runtime repeats and no speedup scoring.

## Claim boundary

- preflight only
- not a speedup result
- PostgreSQL only
- derived from prior checker-backed Direct LLM run artifacts

## Verification

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-expanded-perf-direct-llm-speedup-preflight`
- `python -m json.tool reports/formal_expansion/expanded_perf_direct_llm_speedup_preflight_v0.json >/dev/null`
- `python -m scripts.cli formal-expanded-perf-direct-llm-speedup-preflight --execute || true`
- `python -m json.tool reports/formal_expansion/expanded_perf_direct_llm_speedup_preflight_execute_refused_v0.json >/dev/null`
