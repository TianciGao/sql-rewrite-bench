# Direct LLM Same-Engine Generation 01

## Scope

- denominator_id: `common_core_v0_40`
- method_id: `direct_llm`
- route_id: `direct_llm_same_engine_rewrite`
- planned rows: `120`
- cases: all `40` Common-core v0 cases
- engines: `pg`, `mysql`, `spark`
- one rewrite candidate per `case_id x engine` row

## Boundaries

- Uses an OpenAI-compatible API for generation only.
- Does not run databases.
- Does not execute SQL.
- Does not compute validity, timing, speedup, or leaderboard outputs.
- Does not create `run_event_long.csv` in this run.
- Does not modify case files, registry files, `README`, or `docs/EXECUTION_STATUS.md`.

## Inputs

- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_protocol.md`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_prompt_template.md`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_matrix.csv`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_run_plan.json`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_canary_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_canary_01/run_direct_llm_generation_canary.py`

## Matrix Shape

- performance: `48` rows
- consistency: `27` rows
- portability: `27` rows
- longtail: `18` rows
- pg: `40` rows
- mysql: `40` rows
- spark: `40` rows

## Output Contract

- Prompt audit files: `prompts/<case_id>/<engine>/prompt.txt`
- Raw response audit files: `raw_responses/<case_id>/<engine>/response.txt`
- Successful generations only: `generated/<case_id>/<engine>/direct_llm_same_engine_rewrite.sql`
- All `120` planned rows remain explicit in `run_results.json`
- Post-check status per row:
  - `success`
  - `format_violation`
  - `generation_failed`
