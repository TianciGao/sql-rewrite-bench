# EXPANDED_PERF_DIRECT_LLM_RUN_SCAFFOLD_SUMMARY_v0

## Scope

- Command added: `python -m scripts.cli formal-expanded-perf-direct-llm-run`
- Benchmark line: expanded PERF Direct LLM rewrite
- Case packet size: `34`
- Engine scope: PostgreSQL only
- Route: `LLM_DIRECT_REWRITE_STRONG`

## Command registration status

- Registered in `scripts/cli.py`: `yes`
- Supported options:
  - `--case-id CASE_ID` repeatable
  - `--execute`
  - `--output reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`
- Default mode: dry-run

## Dry-run result

- Command run:
  - `python -m scripts.cli formal-expanded-perf-direct-llm-run --case-id PERF_0007`
- Result: `ok=true`
- Selected case count: `1`
- `PERF_0007` dry-run status: `ready_for_execute`
- Report path: `reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`

## API env status

- API key: `<set>`
- API base URL: `<set>`
- Provider mode: `openai_compatible_base_url`
- Visible env family accepted by scaffold:
  - key: `LLM_API_KEY` or `OPENAI_API_KEY`
  - base URL: `LLM_BASE_URL` or `OPENAI_BASE_URL` or `OPENAI_API_BASE`

## Canary result

- Command run:
  - `source scripts/env_postgres.sh && python -m scripts.cli formal-expanded-perf-direct-llm-run --case-id PERF_0007 --execute`
- Result: `ok=false`
- Call layer result: `failed`
- Failure category: `APIConnectionError`
- Error message: `Connection error.`
- PostgreSQL env visible during canary: `true`
- PostgreSQL execution result: `not_attempted`
- Reason SQL execution did not start: model call failed before SQL extraction
- Report JSON validation:
  - `python -m json.tool reports/formal_expansion/expanded_perf_direct_llm_run_v0.json >/dev/null`
  - result: `passed`

## Full 34-case run readiness

- CLI scaffold readiness: `yes`
- Dry-run readiness for the tested canary path: `yes`
- Full 34-case execution readiness right now: `no`
- Current blocking point: reachable Direct LLM API call path is not healthy in this environment because the canary failed with `APIConnectionError`

## Boundaries

- No registry file changed
- `docs/EXECUTION_STATUS.md` not changed
- No formal review file changed
- No taxonomy calibration note touched
- No full 34-case execution was run
- Only the single requested canary case `PERF_0007` was attempted
